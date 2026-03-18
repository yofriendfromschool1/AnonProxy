<div align="center">
  <img src="https://raw.githubusercontent.com/user/repo/main/extension/icons/icon.png" alt="AnonProxy Logo" width="128" height="128">
  <h1>AnonProxy Anti-Censorship Suite</h1>
  <p>Two independent, zero-log proxy tools built for maximum privacy and bypassing network blocks.</p>
</div>

---

## 🚀 Overview

**AnonProxy** provides two completely independent tools depending on your needs:
1. **The Desktop System Proxy**: A robust, Python-based daemon that acts like Tor or Psiphon, rotating through obfuscated nodes and fallback proxies globally to ensure your entire system stays online in censored environments.
2. **The Safari/Chrome Browser Extension**: A lightweight, standalone extension that securely fetches and injects secure proxy nodes directly to your browser memory—no desktop app required.

Zero data collection. Zero sign-ups. Pure privacy.

## 🔥 The Desktop App (System-wide Bypass)

If your network is heavily censored and you need an aggressive, Lantern/Tor-style background proxy for all traffic on your machine:

1. Ensure **Python 3** is installed.
2. Run the local proxy daemon:
   ```bash
   cd AnonProxy/desktop-app
   python3 app.py
   ```
3. **How it works:** `app.py` rapidly tests hundreds of SOCKS5 nodes concurrently from multiple backup APIs. It instantly drops dead nodes and automatically rotates to working ones if a connection drops, ensuring you always have a bypass.
4. Point your OS proxy settings or CLI tools (like `curl --socks5 127.0.0.1:8080`) to the local port.

## 🦊 The Chrome Extension (Browser Only)

If you only want your browser traffic anonymized without installing or running any system-wide scripts:

1. Open Google Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer mode** using the toggle in the top right corner.
3. Click the **Load unpacked** button in the top left.
4. Select the `AnonProxy/extension` folder.
5. Click **Connect** in the extension popup. The extension independently fetches working proxy nodes from secure APIs and natively tunnels your browser traffic through them.

## ✨ Anti-Censorship Features

- **Concurrent Node Testing:** Tests 200+ nodes simultaneously to instantly establish a connection without waiting minutes for timeouts.
- **Failover APIs:** If one proxy list API is blocked by a firewall, AnonProxy queries GitHub raw content lists or alternative backend APIs seamlessly.
- **Auto-Rotation:** If a node drops or gets blocked mid-session, the Python daemon detects the socket closure and seamlessly negotiates a new route for the next request.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! 
Feel free to check out the [issues page](https://github.com/yofriendfromschool1/AnonProxy/issues).

## 📝 License

This project is open-source and available under the MIT License.
