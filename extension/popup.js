// popup.js

document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('toggle-btn');
  const statusText = document.getElementById('status-text');
  const statusIndicator = document.getElementById('status-indicator');
  const hostInput = document.getElementById('proxy-host');
  const portInput = document.getElementById('proxy-port');

  let isConnected = false;

  // Load saved state
  chrome.storage.local.get(['proxyEnabled', 'host', 'port'], (result) => {
    if (result.host) hostInput.value = result.host;
    if (result.port) portInput.value = result.port;
    
    if (result.proxyEnabled) {
      setConnectedState();
    } else {
      setDisconnectedState();
    }
  });

  toggleBtn.addEventListener('click', () => {
    if (isConnected) {
      // Disable proxy
      chrome.runtime.sendMessage({ action: "disable_proxy" }, (response) => {
        if (response && response.status === "disabled") {
          setDisconnectedState();
        }
      });
    } else {
      // Enable proxy
      const host = hostInput.value.trim() || "127.0.0.1";
      const port = portInput.value.trim() || "8080";
      
      chrome.runtime.sendMessage({ 
        action: "enable_proxy", 
        host: host, 
        port: port 
      }, (response) => {
        if (response && response.status === "enabled") {
          setConnectedState();
        }
      });
    }
  });

  function setConnectedState() {
    isConnected = true;
    statusText.innerText = "Status: Connected";
    statusIndicator.className = "indicator connected";
    toggleBtn.innerText = "Disconnect";
    toggleBtn.className = "disable";
    hostInput.disabled = true;
    portInput.disabled = true;
  }

  function setDisconnectedState() {
    isConnected = false;
    statusText.innerText = "Status: Disconnected";
    statusIndicator.className = "indicator disconnected";
    toggleBtn.innerText = "Connect";
    toggleBtn.className = "enable";
    hostInput.disabled = false;
    portInput.disabled = false;
  }
});
