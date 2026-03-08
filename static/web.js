// web.js

function handleKeyDown(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        summarizeWeb();
    }
}

function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

async function summarizeWeb() {
    const urlInput = document.getElementById('urlInput');
    const summarizeBtn = document.getElementById('summarizeBtn');
    const resultSection = document.getElementById('resultSection');
    const loadingState = document.getElementById('loadingState');
    const resultContent = document.getElementById('resultContent');
    const errorState = document.getElementById('errorState');
    const summaryText = document.getElementById('summaryText');
    const errorText = document.getElementById('errorText');

    const url = urlInput.value.trim();
    if (!url) {
        urlInput.focus();
        return;
    }

    try {
        new URL(url);
    } catch (e) {
        alert("Please enter a valid URL.");
        urlInput.focus();
        return;
    }

    urlInput.disabled = true;
    summarizeBtn.disabled = true;
    resultSection.style.display = 'block';
    loadingState.style.display = 'flex';
    resultContent.style.display = 'none';
    errorState.style.display = 'none';

    // Get or create UUID for this session
    let userId = sessionStorage.getItem('webUserId');
    if (!userId) {
        userId = generateUUID();
        sessionStorage.setItem('webUserId', userId);
    }

    try {
        const response = await fetch(`/web/web_summerizer?url=${encodeURIComponent(url)}`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'user_id': userId // Use dynamically generated UUID
            }
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        
        loadingState.style.display = 'none';
        
        if (data && data.data) {
            resultContent.style.display = 'block';
            summaryText.innerHTML = marked.parse(data.data);
        } else {
            throw new Error("No summary returned from server. Check server logs.");
        }
        
    } catch (error) {
        console.error("Summarization error:", error);
        loadingState.style.display = 'none';
        errorState.style.display = 'flex';
        errorText.textContent = error.message || "Failed to summarize the URL. Please try again.";
    } finally {
        urlInput.disabled = false;
        summarizeBtn.disabled = false;
        urlInput.focus();
    }
}
