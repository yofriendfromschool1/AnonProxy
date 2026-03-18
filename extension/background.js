// background.js
// Handles proxy configuration via chrome.proxy API

// Listen for updates from the popup to enable or disable the proxy
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "enable_proxy") {
    enableProxy(request.host, request.port);
    sendResponse({ status: "enabled" });
  } else if (request.action === "disable_proxy") {
    disableProxy();
    sendResponse({ status: "disabled" });
  }
});

function enableProxy(host, port) {
  const config = {
    mode: "fixed_servers",
    rules: {
      singleProxy: {
        scheme: "http", // Assuming the local desktop app exposes an HTTP proxy initially. We can change to socks5 later.
        host: host,
        port: parseInt(port)
      },
      bypassList: ["127.0.0.1", "localhost"]
    }
  };

  chrome.proxy.settings.set(
    { value: config, scope: "regular" },
    function() {
      if (chrome.runtime.lastError) {
        console.error("Failed to set proxy:", chrome.runtime.lastError);
      } else {
        console.log(`Proxy enabled: ${host}:${port}`);
        // Store state
        chrome.storage.local.set({ proxyEnabled: true, host: host, port: port });
      }
    }
  );
}

function disableProxy() {
  chrome.proxy.settings.clear(
    { scope: "regular" },
    function() {
      if (chrome.runtime.lastError) {
        console.error("Failed to clear proxy:", chrome.runtime.lastError);
      } else {
        console.log("Proxy disabled");
        // Store state
        chrome.storage.local.set({ proxyEnabled: false });
      }
    }
  );
}

// Ensure the proxy is cleared on extension install/update
chrome.runtime.onInstalled.addListener(() => {
    disableProxy();
});
