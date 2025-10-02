// WebSocket connection
let ws = null;
let clientId = 'user_' + Math.random().toString(36).substr(2, 9);
let recognition = null;
let isListening = false;

// Connect to WebSocket
function connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/api/v1/ws/chat/${clientId}`;
    
    ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
        console.log('WebSocket connected');
        showToast('Connected to AI Assistant', 'success');
    };
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.type === 'typing') {
            showTypingIndicator();
        } else if (data.type === 'message') {
            hideTypingIndicator();
            addMessage(data.content, 'agent');
            
            // Speak the response if voice is enabled
            if (document.getElementById('voiceButton').classList.contains('listening')) {
                speak(data.content);
            }
        }
    };
    
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        showToast('Connection error', 'error');
    };
    
    ws.onclose = () => {
        console.log('WebSocket closed');
        setTimeout(connectWebSocket, 3000); // Reconnect after 3 seconds
    };
}

// Initialize Web Speech API
function initVoiceRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            document.getElementById('chatInput').value = transcript;
            sendMessage();
        };
        
        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            stopListening();
        };
        
        recognition.onend = () => {
            stopListening();
        };
    }
}

// Toggle voice listening
function toggleVoice() {
    if (!recognition) {
        showToast('Voice recognition not supported', 'error');
        return;
    }
    
    if (isListening) {
        stopListening();
    } else {
        startListening();
    }
}

function startListening() {
    recognition.start();
    isListening = true;
    document.getElementById('voiceButton').classList.add('listening');
    showToast('Listening...', 'info');
}

function stopListening() {
    if (recognition) {
        recognition.stop();
    }
    isListening = false;
    document.getElementById('voiceButton').classList.remove('listening');
}

// Text-to-Speech
function speak(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        speechSynthesis.speak(utterance);
    }
}

// Send message
function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message || !ws || ws.readyState !== WebSocket.OPEN) {
        return;
    }
    
    addMessage(message, 'user');
    
    ws.send(JSON.stringify({
        type: 'chat',
        message: message,
        context: {
            timestamp: new Date().toISOString()
        }
    }));
    
    input.value = '';
}

// Add message to chat
function addMessage(content, type) {
    const messagesDiv = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    if (type === 'agent') {
        contentDiv.innerHTML = `<strong>Agentice</strong><p class="mb-0 mt-1">${content}</p>`;
    } else {
        contentDiv.innerHTML = `<p class="mb-0">${content}</p>`;
    }
    
    messageDiv.appendChild(contentDiv);
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Typing indicator
function showTypingIndicator() {
    document.getElementById('typingIndicator').classList.add('active');
}

function hideTypingIndicator() {
    document.getElementById('typingIndicator').classList.remove('active');
}

// Quick actions
function quickAction(action) {
    const actions = {
        'search': 'Search for Python developer jobs in Remote',
        'resume': 'Analyze and optimize my resume',
        'cover': 'Help me write a cover letter',
        'status': 'Show my application status'
    };
    
    document.getElementById('chatInput').value = actions[action];
    sendMessage();
}

// Toast notification
function showToast(message, type = 'info') {
    const toastBody = document.getElementById('toastBody');
    const toast = document.getElementById('liveToast');
    
    toastBody.textContent = message;
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

// Auto-apply toggle
document.getElementById('autoApplyToggle').addEventListener('change', (e) => {
    if (e.target.checked) {
        showToast('Auto-apply mode enabled', 'success');
    } else {
        showToast('Auto-apply mode disabled', 'info');
    }
});

// Enter key to send
document.getElementById('chatInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Fetch stats
async function updateStats() {
    try {
        const response = await fetch('/api/v1/applications/stats');
        if (response.ok) {
            const stats = await response.json();
            document.getElementById('appsToday').textContent = stats.today || 0;
            document.getElementById('interviews').textContent = stats.interviews || 0;
            document.getElementById('responses').textContent = stats.responses || 0;
            document.getElementById('successRate').textContent = (stats.success_rate || 0) + '%';
        }
    } catch (error) {
        console.error('Error fetching stats:', error);
    }
}

// Job search functionality
async function startJobSearch() {
    try {
        const response = await fetch('/api/v1/applications/auto-search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                keywords: document.getElementById('keywords')?.value || 'Python Developer',
                location: document.getElementById('location')?.value || 'Remote',
                auto_apply: document.getElementById('autoApplyToggle')?.checked || false
            })
        });
        
        if (response.ok) {
            const result = await response.json();
            showToast(`Job search started! Found ${result.jobs_found || 0} jobs`, 'success');
            updateStats();
        } else {
            showToast('Job search failed. Using chat instead...', 'warning');
            // Fallback to chat
            document.getElementById('chatInput').value = 'Search for Python developer jobs';
            sendMessage();
        }
    } catch (error) {
        console.error('Search error:', error);
        // Fallback to chat-based search
        document.getElementById('chatInput').value = 'Search for Python developer jobs';
        sendMessage();
    }
}

// Load applications
async function loadApplications() {
    try {
        const response = await fetch('/api/v1/applications');
        if (response.ok) {
            const apps = await response.json();
            // Display applications (you can customize this)
            console.log('Applications loaded:', apps);
            showToast(`Loaded ${apps.length || 0} applications`, 'info');
        }
    } catch (error) {
        console.error('Error loading applications:', error);
        // Silently fail - not critical
    }
}

// Refresh applications
function refreshApplications() {
    loadApplications();
}

// Handle search form submit
function handleSearchSubmit(event) {
    if (event) {
        event.preventDefault();
    }
    startJobSearch();
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    connectWebSocket();
    initVoiceRecognition();
    updateStats();
    
    // Update stats every 30 seconds
    setInterval(updateStats, 30000);
    
    // Load applications if table exists
    if (document.getElementById('applicationsTable')) {
        loadApplications();
    }
});
