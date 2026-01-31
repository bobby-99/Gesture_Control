console.log("Cloud VM Gesture Control Loaded");
async function fetchStatus() {
  try {
    const res = await fetch("http://127.0.0.1:5000/status");
    const data = await res.json();

    document.getElementById("connection").innerText = "🟢 Backend Connected";
    document.getElementById("gesture").innerText = data.gesture;
    document.getElementById("action").innerText = data.action;
  } catch (e) {
    document.getElementById("connection").innerText = "🔴 Backend Not Connected";
  }
}

// Refresh every 1 second
setInterval(fetchStatus, 1000);