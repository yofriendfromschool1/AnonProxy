import socket
import select
import threading
import json
import urllib.request
import struct
import platform

# ProxyNode represents a single SOCKS5 proxy from an API
class ProxyNode:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = int(port)

current_proxy = None

def fetch_proxy():
    global current_proxy
    print("Fetching new SOCKS5 proxy...")
    url = "https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc&protocols=socks5"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if not data.get('data'):
                print("No proxies found from API.")
                return False

            for node in data['data']:
                try:
                    ip = node['ip']
                    port = int(node['port'])
                    print(f"Testing proxy: {ip}:{port}")
                    
                    # Quick check if auth is required / host is reachable
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(3.0)
                    s.connect((ip, port))
                    
                    # SOCKS5 greeting
                    s.sendall(b"\x05\x01\x00")
                    greeting_resp = s.recv(2)
                    if not greeting_resp or greeting_resp[0] != 5 or greeting_resp[1] == 0xFF:
                        s.close()
                        continue
                        
                    s.close()
                    print(f"Selected valid proxy: {ip}:{port}")
                    current_proxy = ProxyNode(ip, port)
                    return True
                except Exception as e:
                    pass
    except Exception as e:
        print(f"Failed to fetch proxies: {e}")
    return False

def handle_client(client_socket):
    global current_proxy
    
    if not current_proxy:
        print("No upstream proxy available.")
        client_socket.close()
        return

    req_data = client_socket.recv(4096)
    if not req_data:
        client_socket.close()
        return

    # SOCKS5 upstream connection
    upstream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        upstream.settimeout(5.0)
        upstream.connect((current_proxy.ip, current_proxy.port))
        
        # SOCKS5 Handshake
        upstream.sendall(b"\x05\x01\x00")
        if upstream.recv(2) != b"\x05\x00":
            raise Exception("SOCKS5 auth failed")

        # Reconstruct the target from the initial HTTP request
        try:
            lines = req_data.split(b'\r\n')
            first_line = lines[0].decode()
            method, url, version = first_line.split()
            
            host, port = "", 80
            if method == 'CONNECT':
                host, port = url.split(':')
                port = int(port)
            else:
                parsed_url = urllib.parse.urlparse(url)
                host = parsed_url.hostname
                port = parsed_url.port if parsed_url.port else (443 if parsed_url.scheme == 'https' else 80)
            
            print(f"Proxying request to {host}:{port} via {current_proxy.ip}:{current_proxy.port}")
            
            # Send SOCKS5 connect command
            req = b"\x05\x01\x00\x03" + bytes([len(host)]) + host.encode() + struct.pack(">H", port)
            upstream.sendall(req)
            resp = upstream.recv(10)
            if resp[1] != 0x00:
                raise Exception("SOCKS5 connect failed")

            if method == 'CONNECT':
                client_socket.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")
            else:
                upstream.sendall(req_data)

            # Route traffic
            sockets = [client_socket, upstream]
            while True:
                r, w, e = select.select(sockets, [], [], 10)
                if not r:
                    break
                for s in r:
                    data = s.recv(8192)
                    if not data:
                        break
                    if s is client_socket:
                        upstream.sendall(data)
                    else:
                        client_socket.sendall(data)
                else:
                    continue
                break
        except Exception as e:
            print(f"Error parsing request or routing: {e}")
            
    except Exception as e:
        print(f"Upstream connection error: {e}")
    finally:
        client_socket.close()
        upstream.close()

def start_server(host='127.0.0.1', port=8080):
    fetch_proxy()
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(100)
    print(f"Started local proxy server on {host}:{port}")
    
    while True:
        try:
            client, addr = server.accept()
            threading.Thread(target=handle_client, args=(client,)).start()
        except KeyboardInterrupt:
            break
            
    server.close()

if __name__ == "__main__":
    start_server()
