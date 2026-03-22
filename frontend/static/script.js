document.addEventListener("DOMContentLoaded", () => {
    fetchHistory();
});

function fetchHistory() {
    fetch('/get_history')
        .then(response => response.json())
        .then(messages => {
            const chatBox = document.getElementById('chat-box');
            const historyContainer = document.getElementById('history-container');
            
            historyContainer.innerHTML = '';
            
            if(messages.length === 0) {
                historyContainer.innerHTML = '<div class="history-item">No recent chats</div>';
                return;
            }
            
            chatBox.innerHTML = '';
            
            messages.forEach(msg => {
                appendMessage(msg.role, msg.content, false);
                
                if(msg.role === 'user') {
                    const snippet = msg.content.length > 25 ? msg.content.substring(0,25) + "..." : msg.content;
                    const historyDiv = document.createElement("div");
                    historyDiv.className = "history-item";
                    historyDiv.innerText = snippet;
                    historyContainer.appendChild(historyDiv);
                }
            });
            scrollToBottom();
        })
        .catch(err => console.error("Error fetching history:", err));
}

function clearHistory() {
    if(!confirm('Are you sure you want to delete all your chat history? This cannot be undone.')) return;
    
    fetch('/delete_history', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if(data.success) {
                document.getElementById('history-container').innerHTML = '<div class="history-item">No recent chats</div>';
                document.getElementById('chat-box').innerHTML = `
                    <div class="message-wrapper bot-wrapper">
                        <div class="message-bubble bot">
                            Welcome back! I'm the LTCE Assistant AI. Your chat history has been cleared. How can I assist you today?
                        </div>
                    </div>
                `;
            }
        })
        .catch(err => console.error("Error deleting history:", err));
}

function appendMessage(role, text, animate = true) {
    const chatBox = document.getElementById('chat-box');
    const wrapper = document.createElement('div');
    wrapper.className = `message-wrapper ${role}-wrapper`;
    
    const bubble = document.createElement('div');
    bubble.className = `message-bubble ${role}`;
    
    if (typeof marked !== 'undefined') {
        marked.setOptions({ breaks: true });
        bubble.innerHTML = marked.parse(text);
    } else {
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        bubble.innerHTML = text.replace(urlRegex, function(url) {
            return '<a href="' + url + '" target="_blank" style="color: inherit; text-decoration: underline; font-weight: 500;">' + url + '</a>';
        }).replace(/\n/g, '<br>');
    }
    
    if (animate) {
        wrapper.style.opacity = 0;
        wrapper.style.transform = 'translateY(10px)';
        wrapper.style.transition = 'all 0.3s ease';
    }
    
    wrapper.appendChild(bubble);
    chatBox.appendChild(wrapper);
    
    if (animate) {
        setTimeout(() => {
            wrapper.style.opacity = 1;
            wrapper.style.transform = 'translateY(0)';
        }, 10);
    }
    
    scrollToBottom();
}

function scrollToBottom() {
    const viewport = document.getElementById('chat-viewport');
    viewport.scrollTop = viewport.scrollHeight;
}

function send() {
    let inputField = document.getElementById('msg');
    let message = inputField.value.trim();
    if (!message) return;
    
    appendMessage('user', message);
    inputField.value = '';
    
    const chatBox = document.getElementById('chat-box');
    const typingWrapper = document.createElement('div');
    typingWrapper.className = 'message-wrapper bot-wrapper typing-container';
    typingWrapper.innerHTML = `
        <div class="message-bubble bot typing-bubble" style="padding: 10px 15px;">
            <span></span><span></span><span></span>
        </div>
    `;
    chatBox.appendChild(typingWrapper);
    scrollToBottom();
    
    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector('.typing-container').remove();
        appendMessage('bot', data.reply);
        
        const historyContainer = document.getElementById('history-container');
        if(historyContainer.innerHTML.includes('No recent chats')) {
            historyContainer.innerHTML = '';
        }
        const snippet = message.length > 25 ? message.substring(0,25) + "..." : message;
        const historyDiv = document.createElement("div");
        historyDiv.className = "history-item";
        historyDiv.innerText = snippet;
        historyContainer.insertBefore(historyDiv, historyContainer.firstChild);
    })
    .catch(error => {
        document.querySelector('.typing-container').remove();
        appendMessage('bot', 'Sorry, an error occurred: ' + error.message);
    });
}
