// static/chat.js

// =====================================================
// SESSION MANAGEMENT
// =====================================================

let userId = null;
let uploadedFile = false;
let isConnected = false;

/**
 * Initiates a connection by generating a UUID and storing it in sessionStorage.
 * Reveals the upload panel and chat interface.
 */
function initiateConnection() {
    const btn = document.getElementById('btnConnect');
    btn.classList.add('loading');
    btn.disabled = true;

    // Generate a UUID v4
    userId = crypto.randomUUID();
    sessionStorage.setItem('agentUserId', userId);

    // Simulate a brief connection delay for UX
    setTimeout(() => {
        isConnected = true;
        setConnectedState();
    }, 600);
}

function setConnectedState() {
    // Update status indicator
    const indicator = document.getElementById('statusIndicator');
    indicator.className = 'status-indicator connected';
    indicator.innerHTML = `<span class="status-dot"></span><span id="statusText">Connected</span>`;

    // Hide connect button, show upload + session panels
    document.getElementById('btnConnect').style.display = 'none';
    document.getElementById('uploadPanel').style.display = 'flex';
    document.getElementById('sessionInfo').style.display = 'block';

    // Display truncated session ID
    document.getElementById('sessionIdDisplay').textContent = userId;

    // Remove overlay to reveal chat
    const overlay = document.getElementById('chatOverlay');
    overlay.classList.add('hidden');

    // Enable input
    document.getElementById('messageInput').disabled = false;
    document.getElementById('sendBtn').disabled = false;

    // Show a welcome message
    appendMessage('assistant', '👋 Connected! Upload a PDF or TXT file to give me context, then ask me anything about it.');
}

/**
 * Resets the session – clears storage and reloads the page.
 */
function resetSession() {
    sessionStorage.removeItem('agentUserId');
    location.reload();
}

// =====================================================
// FILE UPLOAD
// =====================================================

async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const statusEl = document.getElementById('uploadStatus');
    const zoneEl = document.getElementById('uploadZone');
    const labelEl = document.getElementById('uploadLabel');

    // Validate file type
    const allowed = ['application/pdf', 'text/plain'];
    const ext = file.name.split('.').pop().toLowerCase();
    if (!allowed.includes(file.type) && !['pdf', 'txt'].includes(ext)) {
        statusEl.textContent = '✗ Only PDF or TXT files are allowed.';
        statusEl.className = 'upload-status error';
        return;
    }

    // Validate single file per session
    if (uploadedFile) {
        statusEl.textContent = '✗ One file per session. Start a new session to upload another.';
        statusEl.className = 'upload-status error';
        return;
    }

    statusEl.textContent = 'Uploading...';
    statusEl.className = 'upload-status';
    zoneEl.classList.remove('uploaded');

    const formData = new FormData();
    formData.append('file', file);

    try {
        const res = await fetch('/uploader/post_content', {
            method: 'POST',
            headers: { 'user_id': userId },
            body: formData
        });

        const data = await res.json();

        if (res.ok) {
            uploadedFile = true;
            zoneEl.classList.add('uploaded');
            labelEl.textContent = `✓ ${file.name}`;
            statusEl.textContent = `Uploaded successfully! The agent is ready.`;
            statusEl.className = 'upload-status';

            appendMessage('assistant', `📄 Document **${file.name}** uploaded successfully! You can now ask me questions about it.`);
        } else {
            statusEl.textContent = `✗ ${data.message || 'Upload failed. Try again.'}`;
            statusEl.className = 'upload-status error';
        }
    } catch (err) {
        statusEl.textContent = '✗ Network error. Please check the server.';
        statusEl.className = 'upload-status error';
        console.error('Upload error:', err);
    }
}

// Drag & Drop support
(function setupDropZone() {
    window.addEventListener('DOMContentLoaded', () => {
        const zone = document.getElementById('uploadZone');
        if (!zone) return;

        zone.addEventListener('dragover', (e) => {
            e.preventDefault();
            zone.classList.add('dragover');
        });

        zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));

        zone.addEventListener('drop', (e) => {
            e.preventDefault();
            zone.classList.remove('dragover');
            const file = e.dataTransfer.files[0];
            if (file) {
                const input = document.getElementById('fileInput');
                // Create a DataTransfer to assign file to the input
                const dt = new DataTransfer();
                dt.items.add(file);
                input.files = dt.files;
                handleFileUpload({ target: input });
            }
        });
    });
})();

// =====================================================
// CHAT MESSAGES
// =====================================================

function appendMessage(role, text) {
    const container = document.getElementById('messagesContainer');

    const msgEl = document.createElement('div');
    msgEl.className = `message ${role}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'user' ? 'U' : 'AI';

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';

    if (role === 'assistant' && typeof marked !== 'undefined') {
        // Render markdown for AI responses (###, **, *, lists etc.)
        bubble.innerHTML = marked.parse(text);
    } else {
        // Plain text for user messages (safe, no XSS risk)
        bubble.textContent = text;
    }

    msgEl.appendChild(avatar);
    msgEl.appendChild(bubble);
    container.appendChild(msgEl);

    container.scrollTop = container.scrollHeight;
    return msgEl;
}


function showTypingIndicator() {
    const container = document.getElementById('messagesContainer');

    const msgEl = document.createElement('div');
    msgEl.className = 'message assistant typing-indicator';
    msgEl.id = 'typingIndicator';

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = 'AI';

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.innerHTML = `<span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>`;

    msgEl.appendChild(avatar);
    msgEl.appendChild(bubble);
    container.appendChild(msgEl);
    container.scrollTop = container.scrollHeight;
}

function removeTypingIndicator() {
    const el = document.getElementById('typingIndicator');
    if (el) el.remove();
}

// =====================================================
// SEND MESSAGE
// =====================================================

async function sendMessage() {
    if (!isConnected || !userId) return;

    const input = document.getElementById('messageInput');
    const text = input.value.trim();
    if (!text) return;

    // Clear input
    input.value = '';
    input.style.height = 'auto';

    // Disable while waiting
    const sendBtn = document.getElementById('sendBtn');
    sendBtn.disabled = true;
    input.disabled = true;

    appendMessage('user', text);
    showTypingIndicator();

    try {
        const res = await fetch(`/chat/chat?message=${encodeURIComponent(text)}`, {
            method: 'POST',
            headers: {
                'user_id': userId,
                'Content-Type': 'application/json'
            }
        });

        const data = await res.json();
        removeTypingIndicator();

        if (res.ok) {
            appendMessage('assistant', data.data || 'No response received.');
        } else {
            appendMessage('assistant', `⚠️ Error: ${data.data || 'Something went wrong.'}`);
        }
    } catch (err) {
        removeTypingIndicator();
        appendMessage('assistant', '⚠️ Could not reach the server. Please check your connection.');
        console.error('Chat error:', err);
    } finally {
        sendBtn.disabled = false;
        input.disabled = false;
        input.focus();
    }
}

// =====================================================
// KEYBOARD & AUTO-RESIZE
// =====================================================

function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function autoResize(el) {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 150) + 'px';
}

// =====================================================
// RESTORE SESSION ON PAGE LOAD
// =====================================================

window.addEventListener('DOMContentLoaded', () => {
    const savedId = sessionStorage.getItem('agentUserId');
    if (savedId) {
        userId = savedId;
        // Note: file upload state is not persisted (by design – one file per session means a fresh upload on restore)
        uploadedFile = false;
        isConnected = true;
        setConnectedState();
        // Remove the welcome message for restored sessions
        const msgs = document.getElementById('messagesContainer');
        msgs.innerHTML = '';
        appendMessage('assistant', '🔄 Session restored. Upload a document and start chatting!');
    }
});
