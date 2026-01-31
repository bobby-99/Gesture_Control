const API_URL = "http://127.0.0.1:8000";

// DOM Elements
const backendStatus = document.getElementById('backend-status');
const instanceList = document.getElementById('instance-list');
const logBody = document.getElementById('log-body');

// Check Connection
async function checkHealth() {
    try {
        console.log("Checking backend health...");
        const response = await fetch(`${API_URL}/`);
        if (response.ok) {
            backendStatus.innerHTML = '<span class="dot"></span> Backend: Online';
            backendStatus.classList.add('online');
            console.log("Backend Online");
            return true;
        }
    } catch (e) {
        console.error("Health Check Failed:", e);
        backendStatus.innerHTML = '<span class="dot"></span> Backend: Offline (Check Console)';
        backendStatus.classList.remove('online');
        return false;
    }
}

// Fetch Instances
async function fetchInstances() {
    try {
        const response = await fetch(`${API_URL}/aws/instances`);
        const data = await response.json();
        renderInstances(data);
    } catch (e) {
        console.error("Failed to fetch instances", e);
    }
}

// Render Instances
function renderInstances(instances) {
    if (instances.length === 0) {
        instanceList.innerHTML = '<div class="loading">No AWS Instances Found (Is credential env set?)</div>';
        return;
    }

    instanceList.innerHTML = instances.map(inst => `
        <div class="instance-card ${inst.state}">
            <span class="instance-id">${inst.id}</span>
            <div class="instance-meta">Type: ${inst.type}</div>
            <div class="instance-meta">State: <span style="color: ${getStateColor(inst.state)}">${inst.state.toUpperCase()}</span></div>
            <div class="instance-meta">IP: ${inst.public_ip}</div>
        </div>
    `).join('');
}

function getStateColor(state) {
    switch (state) {
        case 'running': return 'var(--success)';
        case 'stopped': return 'var(--danger)';
        case 'pending': return 'var(--warning)';
        default: return 'var(--text-secondary)';
    }
}

// Fetch Logs
async function fetchLogs() {
    try {
        const response = await fetch(`${API_URL}/logs`);
        const logs = await response.json();
        renderLogs(logs);
    } catch (e) {
        console.error("Failed to fetch logs", e);
    }
}

function renderLogs(logs) {
    logBody.innerHTML = logs.map(log => `
        <tr>
            <td>${new Date(log.timestamp).toLocaleTimeString()}</td>
            <td>Admin</td>
            <td style="color: var(--accent)">${log.gesture_detected || 'Unknown'}</td>
            <td>${log.action}</td>
            <td>${log.status}</td>
        </tr>
    `).join('');
}

// Poll every 2 seconds
setInterval(() => {
    checkHealth();
    fetchInstances();
    fetchLogs();
}, 2000);

// Initial call
checkHealth();
fetchInstances();
fetchLogs();
