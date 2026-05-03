// static/chat.js

function generateUUID() {
    if (typeof crypto !== 'undefined' && crypto.randomUUID) return crypto.randomUUID();
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
        const r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

window.currentThreadId = null;

window.addEventListener('DOMContentLoaded', async () => {
    await loadThreads();
    const threads = await fetch(ROUTES.GET_ALL_THREADS, { headers: AUTH_HEADERS() }).then(r => r.json());
    if (threads.threads && threads.threads.length > 0) {
        selectThread(threads.threads[0]);
    } else {
        createNewThread();
    }
});

async function loadThreads() {
    const res = await fetch(ROUTES.GET_ALL_THREADS, { headers: AUTH_HEADERS() });
    const data = await res.json();
    const list = document.getElementById('threadsList');
    if (!list) return;
    list.innerHTML = '';
    (data.threads || []).forEach(id => {
        const item = document.createElement('div');
        item.className = 'thread-item' + (window.currentThreadId === id ? ' active' : '');
        item.onclick = () => selectThread(id);
        item.innerHTML = `
            <div style="display: flex; align-items: center; gap: 10px;">
                <span>💬</span>
                <span style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 160px;">Thread ${id.substring(0, 8)}</span>
            </div>
            <button class="delete-thread-btn" onclick="event.stopPropagation(); deleteThread('${id}')">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
            </button>
        `;
        list.appendChild(item);
    });
}

async function deleteThread(id) {
    if (!confirm('Are you sure you want to delete this thread?')) return;
    
    try {
        const res = await fetch(ROUTES.DELETE_THREAD(id), { 
            method: 'DELETE',
            headers: AUTH_HEADERS() 
        });
        if (res.ok) {
            if (window.currentThreadId === id) {
                window.currentThreadId = null;
                document.getElementById('messagesContainer').innerHTML = '<div style="color: #666; text-align: center; padding: 20px;">Thread deleted. Select another or create new.</div>';
                document.getElementById('sessionIdDisplay').textContent = 'Thread ID: ---';
            }
            await loadThreads();
        } else {
            alert('Failed to delete thread');
        }
    } catch (err) {
        console.error('Delete error:', err);
        alert('Error deleting thread');
    }
}

async function selectThread(id) {
    window.currentThreadId = id;
    document.getElementById('sessionIdDisplay').textContent = `Session: ${id.substring(0, 12)}...`;
    const container = document.getElementById('messagesContainer');
    container.innerHTML = '<div style="color: #666; text-align: center; padding: 20px;">Loading conversation...</div>';
    
    try {
        const res = await fetch(ROUTES.LOAD_CONVERSATION(id), { headers: AUTH_HEADERS() });
        const data = await res.json();
        container.innerHTML = '';
        if (data.messages && data.messages.length > 0) {
            data.messages.forEach(msg => {
                const role = msg.type === 'human' ? 'user' : 'assistant';
                appendMessage(role, msg.content || (typeof msg === 'string' ? msg : ''));
            });
        } else {
            appendMessage('assistant', 'Conversation empty. How can I help?');
        }
    } catch (err) {
        container.innerHTML = '<div style="color: #f87171; text-align: center; padding: 20px;">Error loading thread.</div>';
    }
    loadThreads();
}

function createNewThread() {
    const id = generateUUID();
    window.currentThreadId = id;
    document.getElementById('messagesContainer').innerHTML = '';
    document.getElementById('sessionIdDisplay').textContent = `Session: ${id.substring(0, 12)}...`;
    appendMessage('assistant', 'New thread started. I am ready to help!');
    loadThreads();
}

function appendMessage(role, text) {
    const container = document.getElementById('messagesContainer');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'user' ? 'U' : 'AI';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    content.innerHTML = (role === 'assistant' && typeof marked !== 'undefined') ? marked.parse(text) : text;
    
    msgDiv.appendChild(avatar);
    msgDiv.appendChild(content);
    
    // Create a wrapper to center it
    const wrapper = document.createElement('div');
    wrapper.className = 'message-container';
    wrapper.appendChild(msgDiv);
    
    container.appendChild(wrapper);
    container.scrollTop = container.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById('messageInput');
    const text = input.value.trim();
    if (!text) return;
    input.value = '';
    input.style.height = 'auto';
    
    appendMessage('user', text);
    
    const res = await fetch(ROUTES.CHAT_MESSAGE(text), {
        method: 'POST',
        headers: AUTH_HEADERS()
    });
    const data = await res.json();
    if (res.ok) {
        appendMessage('assistant', data.data || 'No response');
        loadThreads();
    }
}

function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function autoResize(el) {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 200) + 'px';
}

// Modal functions
function showUrlModal() { document.getElementById('urlModal').style.display = 'flex'; }
function hideUrlModal() { document.getElementById('urlModal').style.display = 'none'; }
async function handleUrlUpload() {
    const url = document.getElementById('urlInput').value.trim();
    if (!url) return;
    const status = document.getElementById('urlUploadStatus');
    status.textContent = 'Processing...';
    const res = await fetch(ROUTES.UPLOAD_URL(url), { method: 'POST', headers: AUTH_HEADERS() });
    if (res.ok) {
        status.textContent = '✓ Success';
        appendMessage('assistant', `Website **${url}** integrated.`);
        setTimeout(hideUrlModal, 1000);
    } else {
        status.textContent = '✗ Error';
    }
}

async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(ROUTES.UPLOAD_FILE, {
        method: 'POST',
        headers: { 'user_id': getUserId(), 'thread_id': window.currentThreadId },
        body: formData
    });
    if (res.ok) {
        appendMessage('assistant', `File **${file.name}** uploaded.`);
    }
}
