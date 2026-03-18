<div align="center">
  <img src="extension/icons/icon.png" alt="AnonProxy Logo" width="128" height="128">
  <h1>AnonProxy</h1>
  <p>A zero-log, anonymous Chrome extension & local desktop proxy built for maximum privacy.</p>
</div>

---

## 🚀 Overview

**AnonProxy** is a lightweight, cross-platform proxy solution that seamlessly routes your browser traffic through free, dynamically fetched SOCKS5 nodes across the globe. It mimics the behavior of tools like Tor, Psiphon, and Lantern without requiring complex setups or paid subscriptions.

Zero data collection. Zero sign-ups. Pure privacy.

## ✨ Features

- **Dynamic IP Rotation:** The desktop application automatically fetches and validates free public SOCKS5 proxies.
- **Chrome Integration:** A seamless Manifest V3 Chrome extension to toggle your proxy state with a single click.
- **Cross-Platform:** The Python-based local node runs anywhere (Windows, macOS, Linux).
- **Zero Configuration:** No need to manually search for proxies; the desktop app handles fetching, verifying, and routing.

## 🏗️ Architecture

AnonProxy consists of two core components working in tandem:

1. **The Desktop Node (`/desktop-app`):** 
   A lightweight Python server (`127.0.0.1:8080`) that fetches public SOCKS5 proxies from APIs (such as Geonode). It multiplexes incoming browser connections and securely tunnels them through the remote SOCKS5 node.
2. **The Chrome Extension (`/extension`):** 
   A user-friendly frontend that utilizes the `chrome.proxy` API to force Chrome to route all HTTP/HTTPS traffic exclusively through the local Desktop Node.

```text
[Your Browser] ---> [Local Python App (127.0.0.1)] ---> [Public SOCKS5 Node] ---> [Target Website]
```

## 🛠️ Installation & Usage

### 1. Start the Local Proxy Desktop App

Ensure you have **Python 3** installed on your system. No external dependencies are required.

```bash
git clone https://github.com/yourusername/AnonProxy.git
cd AnonProxy/desktop-app
python3 app.py
```

*Expected Output:*
```text
Fetching new SOCKS5 proxy...
Testing proxy: 198.51.100.24:1080
Selected valid proxy: 198.51.100.24:1080
Started local proxy server on 127.0.0.1:8080
```

### 2. Install the Chrome Extension

1. Open Google Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer mode** using the toggle in the top right corner.
3. Click the **Load unpacked** button in the top left.
4. Select the `extension` folder located inside your cloned repository.

### 3. Connect

1. Pin the **AnonProxy** icon to your Chrome toolbar.
2. Click the extension icon to reveal the popup menu.
3. Click **Connect**. The indicator will turn green.
4. Navigate to [IPLEAK.net](https://ipleak.net) to verify that your IP address matches the remote SOCKS5 proxy and your real IP is hidden.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! 
Feel free to check out the [issues page](https://github.com/yofriendfromschool1/AnonProxy/issues) if you have any ideas on how to improve the proxy rotation logic or extension UI.

## 📝 License

This project is open-source and available under the MIT License.
