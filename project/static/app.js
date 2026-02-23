let currentUser = null;
let currentClassId = null;
let enrolledClasses = [];
let selectedQuestionId = null;
let allQuestions = [];
let websocket = null;
let allKbs = [];
let selectedKb = null;
let activeKbName = null;
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 5;

const API_BASE = '/api';

// ============================================================================
// Utility Functions
// ============================================================================

function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
}

function showError(elementId, message) {
    const errorEl = document.getElementById(elementId);
    if (errorEl) {
        errorEl.textContent = message;
        errorEl.classList.remove('hidden');
    }
}

function hideError(elementId) {
    const errorEl = document.getElementById(elementId);
    if (errorEl) {
        errorEl.classList.add('hidden');
    }
}

function getToken() {
    return localStorage.getItem('access_token');
}

function setToken(token) {
    localStorage.setItem('access_token', token);
}

function clearToken() {
    localStorage.removeItem('access_token');
}

function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function renderMarkdown(content) {
    // 1. Protect Math: Replace $...$ and $$...$$ with placeholders
    // We use a specific placeholder format that marked() won't touch.
    const mathBlocks = [];
    
    // Regex for:
    // 1. Display math $$...$$
    // 2. Display math \[...\] (standard LaTeX)
    // 3. Inline math \(...\) (standard LaTeX)
    // 4. Inline math $...$
    // 5. Display math [ ... ] (variant sometimes seen, ensure it contains backslash to avoid false positives with links)
    
    // We use a replacer function to handle them all.
    // Order matters! Display math first.
    
    // Regex explanation:
    // \$\$([\s\S]*?)\$\$ -> $$ ... $$
    // \\\[([\s\S]*?)\\\] -> \[ ... \]  (literal \[ ... \])
    // \\\(([\s\S]*?)\\\) -> \( ... \)  (literal \( ... \))
    // \$([^$\n]*?)\$     -> $ ... $    (inline, no newlines usually, but avoiding double match)
    // \[(\s*\\[\s\S]*?)\] -> [ ... ]    (brackets containing a backslash command roughly)
    
    const regex = /\$\$([\s\S]*?)\$\$|\\\[([\s\S]*?)\\\]|\[(\s*\\[\s\S]*?)\]|\\\(([\s\S]*?)\\\)|\$([^$\n]*?)\$/g;
    
    let protectedContent = content.replace(regex, function(match, m1, m2, m3, m4, m5) {
        const id = `MATH_BLOCK_${mathBlocks.length}`;
        // Normalize to $$...$$ or $...$ depending on the match type
        // m1: $$...$$ content
        // m2: \[...\] content
        // m3: [ ... ] content (our special case)
        // m4: \(...\) content
        // m5: $...$ content
        
        // We want to store the *normalized* version for restoration
        if (m1 !== undefined) mathBlocks.push(`$$${m1}$$`); // Already $$
        else if (m2 !== undefined) mathBlocks.push(`$$${m2}$$`); // Convert \[ to $$
        else if (m3 !== undefined) mathBlocks.push(`$$${m3}$$`); // Convert [ ] with backslash to $$
        else if (m4 !== undefined) mathBlocks.push(`$${m4}$`);  // Convert \( to $
        else if (m5 !== undefined) mathBlocks.push(`$${m5}$`);  // Already $
        else mathBlocks.push(match); // Fallback
        
        return id;
    });

    // 2. Configure marked
    const renderer = new marked.Renderer();
    const linkRenderer = renderer.link;
    renderer.link = (href, title, text) => {
        const html = linkRenderer.call(renderer, href, title, text);
        // Replace <a with the styled version. Use /<a / instad of /^<a / to be safer against whitespace or unexpected prefixes
        const newHtml = html.replace(/<a /, '<a target="_blank" rel="noopener noreferrer" class="citation-link" ');
        return newHtml;
    };

    // 3. Parse markdown
    let html = marked.parse(protectedContent, { renderer: renderer });
    
    // 4. Restore Math
    mathBlocks.forEach((match, index) => {
        const id = `MATH_BLOCK_${index}`;
        html = html.replace(id, match);
    });
    
    // 5. Create temp element for math rendering
    const temp = document.createElement('div');
    temp.innerHTML = html;
    
    // 6. Render math equations
    if (window.renderMathInElement) {
        renderMathInElement(temp, {
            delimiters: [
                {left: '$$', right: '$$', display: true},
                {left: '$', right: '$', display: false},
                {left: '\\(', right: '\\)', display: false},
                {left: '\\[', right: '\\]', display: true}
            ],
            throwOnError: false
        });
    }
    
    return temp.innerHTML;
}

function showNotification(message, type = 'success') {
    const container = document.getElementById('notification-container');
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.style.borderLeftColor = type === 'success' ? 'var(--success)' : 'var(--accent)';
    notification.innerHTML = `
        <div class="flex items-start gap-3">
            <svg class="w-5 h-5 flex-shrink-0 ${type === 'success' ? 'text-green-500' : 'text-orange-500'}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <div class="flex-1">
                <p class="font-medium text-gray-900">${message}</p>
            </div>
        </div>
    `;
    
    container.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

// ============================================================================
// WebSocket Connection
// ============================================================================

// Global click listener for links in chat messages (Capture phase)
document.addEventListener('click', function(e) {
    // Check if clicked element is a link or inside a link
    const link = e.target.closest('a');
    if (link) {
        // Special handling for citation links - always open in new tab and stop propagation
        if (link.classList.contains('citation-link')) {
            e.preventDefault();
            e.stopPropagation();
            window.open(link.href, '_blank');
            return;
        }

        // Check if the link is inside a message body
        if (link.closest('.message-body')) {
            e.preventDefault();
            e.stopPropagation();
            window.open(link.href, '_blank');
        }
    }
}, true);

function connectWebSocket() {
    const token = getToken();
    if (!token) {
        console.log('No token available for WebSocket connection');
        return;
    }
    
    if (websocket) {
        websocket.close();
    }
    
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws?token=${token}`;
    
    console.log('Connecting to WebSocket...');
    websocket = new WebSocket(wsUrl);
    
    websocket.onopen = () => {
        console.log('WebSocket connected');
        reconnectAttempts = 0;
        updateLiveIndicator(true);
        
        setInterval(() => {
            if (websocket && websocket.readyState === WebSocket.OPEN) {
                websocket.send('ping');
            }
        }, 30000);
    };
    
    websocket.onmessage = (event) => {
        try {
            const message = JSON.parse(event.data);
            handleWebSocketMessage(message);
        } catch (error) {
            console.error('Error parsing WebSocket message:', error);
        }
    };
    
    websocket.onerror = (error) => {
        console.error('WebSocket error:', error);
        updateLiveIndicator(false);
    };
    
    websocket.onclose = () => {
        console.log('WebSocket disconnected');
        updateLiveIndicator(false);
        websocket = null;
        
        if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS && currentUser) {
            reconnectAttempts++;
            const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), 30000);
            console.log(`Reconnecting in ${delay}ms (attempt ${reconnectAttempts}/${MAX_RECONNECT_ATTEMPTS})`);
            setTimeout(connectWebSocket, delay);
        }
    };
}

function updateLiveIndicator(isConnected) {
    const indicator = document.getElementById('live-indicator');
    if (!indicator) return;
    
    if (isConnected) {
        indicator.classList.remove('hidden');
        indicator.classList.add('flex');
    } else {
        indicator.classList.add('hidden');
        indicator.classList.remove('flex');
    }
}

function handleWebSocketMessage(message) {
    console.log('WebSocket message received:', message);
    
    switch (message.type) {
        case 'new_question':
            handleNewQuestion(message.data);
            break;
        
        case 'new_message':
            handleNewMessage(message.data);
            break;
        
        default:
            console.log('Unknown message type:', message.type);
    }
}

function handleNewQuestion(questionData) {
    allQuestions.unshift(questionData);
    
    updateStats();
    renderQuestionsSidebar(allQuestions);
    
    if (currentUser.role === 'instructor') {
        showNotification(`New question from ${questionData.user_email}`, 'success');
    }
}

function handleNewMessage(data) {
    const { question_id, message } = data;
    
    const question = allQuestions.find(q => q.id === question_id);
    if (question) {
        if (!question.messages) {
            question.messages = [];
        }
        question.messages.push(message);
        
        if (message.role === 'instructor') {
            question.status = 'answered';
        }
        
        updateStats();
        renderQuestionsSidebar(allQuestions);
        
        if (selectedQuestionId === question_id) {
            renderQuestionDetail(question);
        }
        
        if (currentUser.role === 'student' && message.role === 'instructor') {
            showNotification('You received a new response!', 'success');
        } else if (currentUser.role === 'instructor' && message.role === 'student') {
            showNotification('Student sent a follow-up', 'success');
        }
    }
}

function disconnectWebSocket() {
    if (websocket) {
        websocket.close();
        websocket = null;
    }
}

// ============================================================================
// API Functions
// ============================================================================

async function apiCall(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            ...options,
            headers
        });
        
        if (response.status === 401) {
            clearToken();
            disconnectWebSocket();
            showAuthView();
            // Let it fall through to extract error details
        }
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Request failed');
        }
        
        return await response.json();
    } catch (error) {
        if (error.message === 'Failed to fetch') {
            throw new Error('Connection failed. Please try again.');
        }
        throw error;
    }
}

// ============================================================================
function setActiveNavBtn(btnId) {
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('bg-blue-50', 'text-primary-dark');
        btn.classList.add('text-secondary');
        btn.classList.remove('text-primary');
    });
    const activeBtn = document.getElementById(btnId);
    if (activeBtn) {
        activeBtn.classList.remove('text-secondary');
        activeBtn.classList.add('bg-blue-50', 'text-primary-dark');
    }
}

function showAuthView() {
    // ...
    // hide all views
    document.getElementById('auth-view').classList.remove('hidden');
    document.getElementById('dashboard-view').classList.add('hidden');
    document.getElementById('kb-view')?.classList.add('hidden');
    document.getElementById('verify-view')?.classList.add('hidden');
    document.getElementById('nav-actions').classList.add('hidden');
    disconnectWebSocket();
    
    document.getElementById('register-success-view')?.classList.add('hidden');
    document.getElementById('login-form')?.classList.remove('hidden');
    document.getElementById('register-form')?.classList.add('hidden');
    document.getElementById('show-login')?.classList.add('bg-white', 'text-primary', 'shadow-sm');
    document.getElementById('show-login')?.classList.remove('text-gray-600');
    document.getElementById('show-register')?.classList.remove('bg-white', 'text-primary', 'shadow-sm');
    document.getElementById('show-register')?.classList.add('text-gray-600');
}

function showDashboardView() {
    document.getElementById('auth-view').classList.add('hidden');
    document.getElementById('dashboard-view').classList.remove('hidden');
    document.getElementById('kb-view')?.classList.add('hidden');
    document.getElementById('classes-view')?.classList.add('hidden');
    document.getElementById('account-settings-view')?.classList.add('hidden');
    document.getElementById('nav-actions').classList.remove('hidden');
    document.getElementById('nav-actions').classList.add('flex');
    setActiveNavBtn('nav-questions-btn');
}

function showKbView() {
    document.getElementById('auth-view').classList.add('hidden');
    document.getElementById('dashboard-view').classList.add('hidden');
    document.getElementById('classes-view')?.classList.add('hidden');
    document.getElementById('account-settings-view')?.classList.add('hidden');
    document.getElementById('kb-view').classList.remove('hidden');
    document.getElementById('nav-actions').classList.remove('hidden');
    document.getElementById('nav-actions').classList.add('flex');
    setActiveNavBtn('kb-btn');
    loadKnowledgeBases();
    fetchActiveKb();
}

function showClassesView() {
    document.getElementById('auth-view').classList.add('hidden');
    document.getElementById('dashboard-view').classList.add('hidden');
    document.getElementById('kb-view')?.classList.add('hidden');
    document.getElementById('account-settings-view')?.classList.add('hidden');
    document.getElementById('classes-view').classList.remove('hidden');
    document.getElementById('nav-actions').classList.remove('hidden');
    document.getElementById('nav-actions').classList.add('flex');
    loadClasses();
}

function showAccountSettingsView() {
    document.getElementById('auth-view').classList.add('hidden');
    document.getElementById('dashboard-view').classList.add('hidden');
    document.getElementById('kb-view')?.classList.add('hidden');
    document.getElementById('classes-view')?.classList.add('hidden');
    document.getElementById('account-settings-view').classList.remove('hidden');
    document.getElementById('nav-actions').classList.remove('hidden');
    document.getElementById('nav-actions').classList.add('flex');
    setActiveNavBtn('account-settings-btn');
}

// ============================================================================
// Stats & Analytics
// ============================================================================

function updateStats() {
    const total = allQuestions.length;
    const answered = allQuestions.filter(q => q.status === 'answered').length;
    const pending = allQuestions.filter(q => q.status === 'pending').length;
    
    const totalEl = document.getElementById('stat-total');
    const answeredEl = document.getElementById('stat-answered');
    const pendingEl = document.getElementById('stat-pending');
    
    if (totalEl) totalEl.textContent = total;
    if (answeredEl) answeredEl.textContent = answered;
    if (pendingEl) pendingEl.textContent = pending;
}

// ============================================================================
// Rendering Functions
// ============================================================================

function renderQuestionsSidebar(questions) {
    const container = document.getElementById('questions-sidebar');
    const searchTerm = document.getElementById('search-questions')?.value.toLowerCase() || '';
    
    let filteredQuestions = questions;
    if (searchTerm) {
        filteredQuestions = questions.filter(q => 
            q.content.toLowerCase().includes(searchTerm) ||
            (q.user_email && q.user_email.toLowerCase().includes(searchTerm))
        );
    }
    
    if (filteredQuestions.length === 0) {
        container.innerHTML = `
            <div class="text-center py-12 text-gray-400">
                <svg class="w-16 h-16 mx-auto mb-3 opacity-40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <p class="text-sm">${searchTerm ? 'No questions found' : 'No questions yet'}</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = filteredQuestions.map(q => {
        const messageCount = q.messages ? q.messages.length : 0;
        const lastMessage = messageCount > 0 ? q.messages[messageCount - 1] : null;
        
        return `
        <div class="question-item ${selectedQuestionId === q.id ? 'active' : ''} 
                    cursor-pointer p-4 rounded-lg mb-2 border border-transparent"
             onclick="selectQuestion(${q.id})">
            <div class="flex items-start justify-between gap-2 mb-2">
                <span class="status-badge status-${q.status}">
                    <span class="status-indicator bg-current"></span>
                    ${q.status}
                </span>
                <span class="text-xs text-gray-500 mono">${formatDate(q.created_at)}</span>
            </div>
            ${(enrolledClasses.find(c => c.id == currentClassId)?.role === 'instructor' || enrolledClasses.find(c => c.id == currentClassId)?.role === 'ta' || enrolledClasses.find(c => c.id == currentClassId)?.role === 'owner') ? `
                <div class="text-xs text-gray-500 mb-1 font-medium">${escapeHtml(q.user_email)}</div>
            ` : ''}
            <p class="text-sm text-gray-800 line-clamp-2 mb-1">${escapeHtml(q.content)}</p>
            ${messageCount > 0 ? `
                <div class="text-xs text-gray-500 flex items-center gap-1 mt-2">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                    </svg>
                    <span>${messageCount} message${messageCount > 1 ? 's' : ''}</span>
                </div>
            ` : ''}
        </div>
    `;
    }).join('');
}

function renderQuestionDetail(question) {
    const container = document.getElementById('question-detail');
    
    if (!question) {
        container.innerHTML = `
            <div class="empty-state">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <h3 class="text-xl font-bold serif mb-2">Select a Question</h3>
                <p class="text-sm">Choose a question from the sidebar to view the conversation</p>
            </div>
        `;
        return;
    }
    
    selectedQuestionId = question.id;
    
    const activeClass = enrolledClasses.find(c => c.id == currentClassId);
    const isStaff = activeClass && (activeClass.role === 'owner' || activeClass.role === 'instructor' || activeClass.role === 'ta');
    const messages = question.messages || [];
    
    container.innerHTML = `
        <div class="max-w-3xl mx-auto animate-slide-in">
            <!-- Question Header -->
            <div class="bg-white rounded-2xl shadow-lg p-6 mb-6">
                <div class="flex items-start justify-between gap-4 mb-4">
                    <div class="flex-1">
                        ${isStaff ? `
                            <div class="flex items-center gap-2 text-sm text-gray-600 mb-2">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                                </svg>
                                <span class="font-medium">${escapeHtml(question.user_email)}</span>
                            </div>
                        ` : ''}
                        <span class="status-badge status-${question.status} text-xs">
                            <span class="status-indicator bg-current"></span>
                            ${question.status}
                        </span>
                    </div>
                    <div class="text-right">
                        <div class="text-xs text-gray-500 mono">${formatDate(question.created_at)}</div>
                        <div class="text-xs text-gray-400 mt-1">#${question.id}</div>
                    </div>
                </div>
                
                <div class="prose max-w-none">
                    <h3 class="text-xl font-bold serif text-gray-900 mb-3">Question</h3>
                    <div class="text-gray-800 leading-relaxed markdown-content">${renderMarkdown(question.content)}</div>
                </div>
            </div>
            
            <!-- Chat Thread -->
            <div class="bg-white rounded-2xl shadow-lg p-6 mb-6">
                <h3 class="text-lg font-bold serif text-gray-900 mb-4">Conversation</h3>
                
                <div class="chat-thread mb-6">
                    ${messages.length === 0 ? `
                        <div class="text-center py-8 text-gray-400">
                            <p class="text-sm">No messages yet. ${isStaff ? 'Be the first to respond!' : 'Waiting for instructor response...'}</p>
                        </div>
                    ` : messages.map(msg => `
                        <div class="message-bubble ${msg.role}" data-message-id="${msg.id}">
                            <div class="message-avatar ${msg.role}">
                                ${msg.role === 'student' ? 'S' : 'I'}
                            </div>
                            <div class="message-content">
                                <div class="message-header">
                                    <span class="message-role">${msg.role === 'student' ? 'Student' : 'Instructor'}</span>
                                    <span class="message-time">${formatDate(msg.created_at)}</span>
                                    ${msg.source ? `<span class="message-source">${msg.source}</span>` : ''}
                                </div>
                                <div class="message-body">
                                    <div class="markdown-content">${renderMarkdown(msg.content)}</div>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
                
                ${isStaff ? `
                    <!-- Instructor Reply Box -->
                    <div class="reply-box">
                        <div id="suggestion-${question.id}" class="hidden suggestion-box mb-4">
                            <div class="flex items-start gap-3">
                                <svg class="w-5 h-5 text-primary flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                                </svg>
                                <div class="flex-1">
                                    <div class="flex items-center gap-2 mb-2">
                                        <span class="text-sm font-semibold text-gray-700">AI Suggestion</span>
                                        <span id="source-${question.id}" class="text-xs px-2 py-0.5 rounded bg-white border border-gray-300 mono"></span>
                                    </div>
                                    <div id="suggested-text-${question.id}" class="text-sm text-gray-700 leading-relaxed"></div>
                                </div>
                            </div>
                        </div>
                        
                        <button 
                            onclick="getSuggestion(${question.id})" 
                            id="suggest-btn-${question.id}"
                            class="btn-secondary mb-4 text-sm">
                            <svg class="w-4 h-4 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                            </svg>
                            Get AI Suggestion
                        </button>

                        <div id="kb-selection-${question.id}" class="mb-4 ${isStaff ? '' : 'hidden'}">
                             <label class="block text-xs font-semibold text-gray-700 mb-1">Select Knowledge Base</label>
                             <select id="kb-select-${question.id}" class="input-field text-sm py-1">
                                 <!-- Options populated by JS -->
                             </select>
                        </div>
                        
                        <textarea 
                            id="reply-input-${question.id}" 
                            class="input-field mb-2"
                            rows="4" 
                            placeholder="Write your response... (Markdown supported)"></textarea>
                        <div class="text-xs text-gray-500 mb-2">
                            Tip: Use **bold**, *italic*, \`code\`, and $math$ for formatting
                        </div>
                        <div id="reply-error-${question.id}" class="text-error text-sm mb-2 hidden"></div>
                        <button 
                            onclick="sendMessage(${question.id})" 
                            class="btn-primary">
                            Send Reply
                        </button>
                    </div>
                ` : `
                    <!-- Student Reply Box -->
                    <div class="reply-box">
                        <textarea 
                            id="reply-input-${question.id}" 
                            class="input-field mb-2"
                            rows="3" 
                            placeholder="Ask a follow-up question..."></textarea>
                        <div id="reply-error-${question.id}" class="text-error text-sm mb-2 hidden"></div>
                        <button 
                            onclick="sendMessage(${question.id})" 
                            class="btn-primary">
                            Send Follow-up
                        </button>
                    </div>
                `}
            </div>
        </div>
    `;
    
    // Scroll to latest message
    setTimeout(() => {
        const chatThread = container.querySelector('.chat-thread');
        if (chatThread && chatThread.lastElementChild) {
            chatThread.lastElementChild.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }, 100);

    // Populate KB select
    if (isStaff) {
        populateKbSelect(question.id);
    }
}

async function populateKbSelect(questionId) {
    const select = document.getElementById(`kb-select-${questionId}`);
    if (!select) return;
    
    // Ensure KBs are loaded
    if (allKbs.length === 0) {
        try {
            const data = await apiCall('/instructor/kbs');
            allKbs = data.kbs || [];
        } catch (e) {
            console.error('Failed to load KBs for select:', e);
        }
    }

    if (!activeKbName && allKbs.length > 0) {
        await fetchActiveKb();
    }
    
    // Clear existing options
    select.innerHTML = '';
    
    // If no KBs, maybe show a placeholder?
    if (allKbs.length === 0) {
        const option = document.createElement('option');
        option.value = "";
        option.textContent = "No KBs Available";
        select.appendChild(option);
        return;
    }
    
    allKbs.forEach(kb => {
        const option = document.createElement('option');
        option.value = kb;
        option.textContent = kb;
        select.appendChild(option);
    });

    // Auto-select active KB
    if (activeKbName) {
        select.value = activeKbName;
    }
}

// ============================================================================
// Question Actions
// ============================================================================

window.selectQuestion = function(questionId) {
    const question = allQuestions.find(q => q.id === questionId);
    if (question) {
        selectedQuestionId = questionId;
        renderQuestionDetail(question);
        renderQuestionsSidebar(allQuestions);
    }
};

window.getSuggestion = async function(questionId) {
    const btnEl = document.getElementById(`suggest-btn-${questionId}`);
    const suggestionBox = document.getElementById(`suggestion-${questionId}`);
    const kbSelect = document.getElementById(`kb-select-${questionId}`);
    let selectedKbName = kbSelect ? kbSelect.value : null;

    if (!selectedKbName && activeKbName) {
        selectedKbName = activeKbName;
    }
    
    btnEl.disabled = true;
    btnEl.innerHTML = `
        <svg class="animate-spin w-4 h-4 inline-block mr-2" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Generating...
    `;
    
    try {
        let url = `/instructor/suggest/${questionId}`;
        if (selectedKbName) {
            url += `?kb_name=${encodeURIComponent(selectedKbName)}`;
        }
        const data = await apiCall(url);
        
        suggestionBox.classList.remove('hidden');
        document.getElementById(`source-${questionId}`).textContent = data.source;
        document.getElementById(`suggested-text-${questionId}`).innerHTML = renderMarkdown(data.suggested_answer);
        document.getElementById(`reply-input-${questionId}`).value = data.suggested_answer;
        
        btnEl.classList.add('hidden');
        showNotification('AI suggestion generated successfully', 'success');
    } catch (error) {
        btnEl.disabled = false;
        btnEl.innerHTML = `
            <svg class="w-4 h-4 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
            Get AI Suggestion
        `;
        showNotification('Error: ' + error.message, 'error');
    }
};

window.sendMessage = async function(questionId) {
    const replyInput = document.getElementById(`reply-input-${questionId}`);
    const content = replyInput.value.trim();
    const errorEl = document.getElementById(`reply-error-${questionId}`);
    
    errorEl.classList.add('hidden');
    
    if (!content) {
        errorEl.textContent = 'Message cannot be empty';
        errorEl.classList.remove('hidden');
        return;
    }
    
    try {
        showLoading();
        
        const suggestionVisible = document.getElementById(`suggestion-${questionId}`) && 
                                 !document.getElementById(`suggestion-${questionId}`).classList.contains('hidden');
        const source = suggestionVisible ? 
            (document.getElementById(`source-${questionId}`).textContent === 'cached' ? 'cached' : 'ai') : 
            'manual';
        
        const activeClass = enrolledClasses.find(c => c.id == currentClassId);
        const isStaff = activeClass && (activeClass.role === 'owner' || activeClass.role === 'instructor' || activeClass.role === 'ta');
        
        await apiCall(`/questions/${questionId}/messages`, {
            method: 'POST',
            body: JSON.stringify({
                content: content,
                source: isStaff ? source : null
            })
        });
        
        replyInput.value = '';
        showNotification('Message sent successfully!', 'success');
        
        // WebSocket will handle updating the UI
        
    } catch (error) {
        errorEl.textContent = error.message;
        errorEl.classList.remove('hidden');
    } finally {
        hideLoading();
    }
};

// ============================================================================
// Load Data
// ============================================================================

async function loadQuestions() {
    try {
        if (!currentClassId) {
            allQuestions = [];
            updateStats();
            renderQuestionsSidebar(allQuestions);
            renderQuestionDetail(null);
            return;
        }

        showLoading();
        
        const activeClass = enrolledClasses.find(c => c.id == currentClassId);
        const isStaff = activeClass && (activeClass.role === 'owner' || activeClass.role === 'instructor' || activeClass.role === 'ta');
        
        let endpoint = isStaff ? '/instructor/questions' : '/questions';
        allQuestions = await apiCall(`${endpoint}?class_id=${currentClassId}`);
        
        updateStats();
        renderQuestionsSidebar(allQuestions);
        
        if (allQuestions.length > 0 && !selectedQuestionId) {
            selectQuestion(allQuestions[0].id);
        } else if (selectedQuestionId) {
            const question = allQuestions.find(q => q.id === selectedQuestionId);
            if (question) {
                renderQuestionDetail(question);
            }
        } else {
            renderQuestionDetail(null);
        }
        
    } catch (error) {
        showNotification('Error loading questions: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function loadCurrentUser() {
    try {
        currentUser = await apiCall('/me');
        console.log("Current user role:", currentUser.role);
        document.getElementById('user-email').textContent = currentUser.email;
        
        if (currentUser.is_instructor_pending) {
            document.getElementById('instructor-pending-banner')?.classList.remove('hidden');
        } else {
            document.getElementById('instructor-pending-banner')?.classList.add('hidden');
        }
        
        if (currentUser.role === 'instructor') {
            document.getElementById('kb-btn').classList.remove('hidden');
            document.getElementById('kb-btn').classList.add('flex');
            document.getElementById('kb-btn').onclick = showKbView;
        } else {
            document.getElementById('kb-btn').classList.add('hidden');
            document.getElementById('kb-btn').classList.remove('flex');
        }

        showDashboardView();

        // Load classes first to set currentClassId
        await loadClasses();
        
        // Load questions for the selected class
        await loadQuestions();
        
        connectWebSocket();
        
    } catch (error) {
        clearToken();
        showAuthView();
    }
}

// ============================================================================
// New Question Modal
// ============================================================================

function showNewQuestionModal() {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
        <div class="modal-content">
            <h3 class="text-2xl font-bold serif mb-6">Ask a New Question</h3>
            <form id="new-question-form">
                <div class="mb-4">
                    <label class="block text-sm font-semibold text-gray-700 mb-2">Your Question</label>
                    <textarea 
                        id="new-question-content" 
                        required 
                        maxlength="10000"
                        class="input-field"
                        rows="6" 
                        placeholder="What would you like to know?"></textarea>
                </div>
                <div id="new-question-error" class="text-error text-sm mb-4 hidden"></div>
                <div class="flex gap-3 justify-end">
                    <button type="button" onclick="this.closest('.modal-overlay').remove()" class="btn-secondary">
                        Cancel
                    </button>
                    <button type="submit" class="btn-primary">
                        Submit Question
                    </button>
                </div>
            </form>
        </div>
    `;
    
    document.body.appendChild(modal);
    document.getElementById('new-question-content').focus();
    
    document.getElementById('new-question-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const content = document.getElementById('new-question-content').value.trim();
        const errorEl = document.getElementById('new-question-error');
        
        errorEl.classList.add('hidden');
        
        if (!currentClassId) {
            errorEl.textContent = 'You must select a class first';
            errorEl.classList.remove('hidden');
            return;
        }
        
        if (!content) {
            errorEl.textContent = 'Question cannot be empty';
            errorEl.classList.remove('hidden');
            return;
        }
        
        try {
            showLoading();
            const res = await apiCall('/questions', {
                method: 'POST',
                body: JSON.stringify({ 
                    content,
                    class_id: currentClassId 
                })
            });
            
            modal.remove();
            showNotification('Question submitted successfully!', 'success');
            
        } catch (error) {
            errorEl.textContent = error.message;
            errorEl.classList.remove('hidden');
        } finally {
            hideLoading();
        }
    });
}

function showCreateKbModal() {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
        <div class="modal-content">
            <h3 class="text-2xl font-bold serif mb-6">Create Knowledge Base</h3>
            <form id="create-kb-form">
                <div class="mb-4">
                    <label class="block text-sm font-semibold text-gray-700 mb-2">Name</label>
                    <input type="text" id="kb-name-input" required class="input-field" placeholder="e.g., Course Content 2024" pattern="[a-zA-Z0-9_-]+" title="Alphanumeric, underscores, and dashes only">
                    <p class="text-xs text-gray-500 mt-1">Only letters, numbers, underscores, and dashes allowed.</p>
                </div>
                
                <div class="mb-6">
                    <label class="block text-sm font-semibold text-gray-700 mb-2">Initial Documents (Optional)</label>
                    <div class="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center cursor-pointer hover:border-primary hover:bg-gray-50 transition-colors" onclick="document.getElementById('create-kb-files').click()">
                        <input type="file" id="create-kb-files" multiple accept=".txt,.md,.pdf" class="hidden">
                        <svg class="w-8 h-8 text-gray-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                        </svg>
                        <p class="text-sm text-gray-600 font-medium">Click to select files</p>
                        <p class="text-xs text-gray-500">.txt, .md, or .pdf</p>
                        <div id="selected-files-count" class="text-xs text-primary font-medium mt-2 hidden"></div>
                    </div>
                </div>

                <!-- File Status List -->
                <div id="kb-upload-status-container" class="mb-4 hidden" style="max-height: 200px; overflow-y: auto;">
                    <label class="block text-sm font-semibold text-gray-700 mb-2">Upload Progress</label>
                    <div id="kb-upload-status-list" class="bg-gray-50 border rounded-lg divide-y text-sm">
                        <!-- Dynamic Status Items -->
                    </div>
                </div>

                <div id="create-kb-error" class="text-error text-sm mb-4 hidden"></div>
                <div class="flex gap-3 justify-end">
                    <button type="button" onclick="this.closest('.modal-overlay').remove()" class="btn-secondary">
                        Cancel
                    </button>
                    <button type="submit" class="btn-primary" id="create-submit-btn">
                        Create KB
                    </button>
                </div>
            </form>
        </div>
    `;
    
    document.body.appendChild(modal);
    document.getElementById('kb-name-input').focus();
    
    // File selection handler
    document.getElementById('create-kb-files').onchange = (e) => {
        const count = e.target.files.length;
        const countEl = document.getElementById('selected-files-count');
        if (count > 0) {
            countEl.textContent = `${count} file${count !== 1 ? 's' : ''} selected`;
            countEl.classList.remove('hidden');
        } else {
            countEl.classList.add('hidden');
        }
    };
    
    document.getElementById('create-kb-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('kb-name-input').value.trim();
        const files = document.getElementById('create-kb-files').files;
        const errorEl = document.getElementById('create-kb-error');
        const submitBtn = document.getElementById('create-submit-btn');
        
        errorEl.classList.add('hidden');
        submitBtn.disabled = true;
        
        try {
            // 1. Create KB
            submitBtn.innerHTML = '<span class="animate-spin inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full mr-2"></span>Creating...';
            
            await apiCall('/instructor/kbs', {
                method: 'POST',
                body: JSON.stringify({ name })
            });

            // 2. Upload Files if any
            if (files.length > 0) {
                const statusContainer = document.getElementById('kb-upload-status-container');
                const statusList = document.getElementById('kb-upload-status-list');
                
                statusContainer.classList.remove('hidden');
                
                // Helper to format size
                const formatSize = (bytes) => {
                    if (bytes < 1024) return bytes + ' B';
                    const k = 1024;
                    const sizes = ['KB', 'MB', 'GB'];
                    const i = Math.floor(Math.log(bytes) / Math.log(k));
                    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i-1]; // i-1 because 0 is B
                };
                
                // Correct helper:
                const getFormattedSize = (file) => {
                    const sizeKB = file.size / 1024;
                    if (sizeKB < 1000) return `(${sizeKB.toFixed(1)} KB)`;
                    return `(${(sizeKB/1024).toFixed(2)} MB)`; 
                };

                // Initialize list with sizes
                statusList.innerHTML = Array.from(files).map((f, i) => `
                    <div id="upload-item-${i}" class="p-2 flex items-center justify-between">
                        <div class="flex items-center gap-2 truncate pr-2">
                             <span class="font-medium text-gray-700">${f.name}</span>
                             <span class="text-xs text-gray-400">${getFormattedSize(f)}</span>
                        </div>
                        <span class="status-icon text-gray-400 text-xs">Pending...</span>
                    </div>
                `).join('');

                let successCount = 0;
                let failCount = 0;

                for (let i = 0; i < files.length; i++) {
                    const row = document.getElementById(`upload-item-${i}`);
                    const statusEl = row.querySelector('.status-icon');
                    const file = files[i];
                    
                    // Check size limit (2MB)
                    if (file.size > 2 * 1024 * 1024) {
                         statusEl.innerHTML = '<span class="text-error font-bold text-xs">Too Large (>2MB)</span>';
                         row.classList.add('bg-red-50');
                         failCount++;
                         continue; // Skip upload
                    }

                    try {
                        statusEl.innerHTML = '<span class="animate-spin inline-block w-3 h-3 border-2 border-primary border-t-transparent rounded-full"></span>';
                        submitBtn.innerHTML = `Uploading (${i + 1}/${files.length})...`;
                        
                        // Use uploadFileToKb helper instead of manual fetch if available, or inline
                        await uploadFileToKb(name, file);
                        
                        statusEl.innerHTML = '<span class="text-green-600 font-bold">✓</span>';
                        row.classList.add('bg-green-50');
                        successCount++;
                    } catch (err) {
                       console.error(`Failed to upload ${file.name}`, err);
                       statusEl.innerHTML = '<span class="text-red-500 font-bold">✗</span>';
                       row.classList.add('bg-red-50');
                       failCount++;
                    }
                }

                if (failCount > 0) {
                     submitBtn.innerHTML = 'Completed with Errors';
                     submitBtn.classList.remove('btn-primary');
                     submitBtn.classList.add('btn-secondary');
                     errorEl.classList.remove('hidden');
                     errorEl.innerHTML = `Created KB <b>${name}</b>.<br>Uploaded ${successCount}/${files.length} files.<br>${failCount} failed or skipped.`;
                     
                     modal.querySelector('.btn-secondary').textContent = "Close";
                     return; 
                }
            }

            modal.remove();
            showNotification(`Knowledge Base '${name}' created successfully`, 'success');
            loadKnowledgeBases();

        } catch (error) {
            errorEl.textContent = error.message;
            errorEl.classList.remove('hidden');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Create KB';
        }
    });
}


// ============================================================================
// Knowledge Base Functions
// ============================================================================


async function uploadFileToKb(kbName, file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const token = getToken();
    const response = await fetch(`${API_BASE}/instructor/kbs/${kbName}/files`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        body: formData
    });

    if (!response.ok) {
        let errorMsg = 'Upload failed';
        try {
            const err = await response.json();
            errorMsg = err.detail || errorMsg;
        } catch (e) {
            errorMsg = response.statusText;
        }
        throw new Error(errorMsg);
    }
    return true;
}

async function fetchActiveKb() {
    try {
        const config = await apiCall('/instructor/config');
        activeKbName = config.active_kb;
        if (allKbs.length > 0) renderKbList(allKbs);
    } catch (e) {
        console.error("Failed to load active KB", e);
    }
}

async function setActiveKb() {
    if (!selectedKb) return;
    try {
        const config = await apiCall('/instructor/config', {
            method: 'POST',
            body: JSON.stringify({ active_kb: selectedKb })
        });
        activeKbName = selectedKb;
        showNotification(`'${selectedKb}' set as Active Knowledge Base`, 'success');
        
        // Update UI
        renderKbList(allKbs);
        updateActiveKbUi(selectedKb);
        
    } catch (e) {
        showNotification("Failed to set active KB", 'error');
    }
}

async function loadKnowledgeBases() {
    try {
        showLoading();
        
        const currentClass = enrolledClasses.find(c => parseInt(c.id) === currentClassId);
        
        if (!currentClass || !currentClass.kb_name) {
            allKbs = [];
            renderKbList([]);
            document.getElementById('kb-details-content').classList.add('hidden');
            document.getElementById('kb-details-content').classList.remove('flex');
            document.getElementById('kb-details-empty').classList.remove('hidden');
            document.getElementById('kb-details-empty').innerHTML = `
                <div class="text-center">
                    <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                    </svg>
                    <h3 class="text-xl font-bold text-gray-700 mb-2">No Knowledge Base Available</h3>
                    <p class="text-gray-500">This class does not have an active Knowledge Base.</p>
                </div>
            `;
            return;
        }

        allKbs = [currentClass.kb_name];
        renderKbList(allKbs);
        await selectKb(currentClass.kb_name);
        
    } catch (error) {
        showNotification('Failed to load KB: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

function renderKbList(kbs) {
    const container = document.getElementById('kb-list');
    container.innerHTML = kbs.map(kb => {
        const isActive = (kb === activeKbName);
        return `
        <div class="kb-item ${selectedKb === kb ? 'active' : ''} cursor-pointer p-4 rounded-lg mb-1"
             onclick="selectKb('${kb}')">
             <div class="flex items-center justify-between">
                 <div class="flex items-center gap-3">
                     <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                         <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"></path>
                     </svg>
                     <span class="font-medium text-gray-700">${kb}</span>
                 </div>
                 ${isActive ? '<span class="w-2.5 h-2.5 rounded-full bg-green-500" title="Active KB"></span>' : ''}
             </div>
        </div>
    `}).join('');
}

async function selectKb(kbName) {
    selectedKb = kbName;
    renderKbList(allKbs);
    
    document.getElementById('kb-details-empty').classList.add('hidden');
    document.getElementById('kb-details-content').classList.remove('hidden');
    document.getElementById('kb-details-content').classList.add('flex');
    document.getElementById('selected-kb-name').textContent = kbName;
    
    updateActiveKbUi(kbName);
    
    await loadKbDetails(kbName);
}

function updateActiveKbUi(kbName) {
    const setBtn = document.getElementById('set-active-kb-btn');
    const badge = document.getElementById('active-kb-badge');
    
    if (kbName === activeKbName) {
        setBtn.classList.add('hidden');
        badge.classList.remove('hidden');
        badge.classList.add('inline-flex'); // or block, depending on layout
    } else {
        setBtn.classList.remove('hidden');
        badge.classList.add('hidden');
        badge.classList.remove('inline-flex');
    }
}

async function loadKbDetails(kbName) {
    try {
        const details = await apiCall(`/instructor/kbs/${kbName}`);
        const files = details.files || [];
        
        document.getElementById('kb-file-count').textContent = `${files.length} file${files.length !== 1 ? 's' : ''}`;
        renderKbFiles(files);
        setupDragAndDrop(kbName);
        
    } catch (error) {
        showNotification('Failed to load KB details', 'error');
    }
}

function renderKbFiles(files) {
    const container = document.getElementById('kb-files-list');
    
    if (files.length === 0) {
        container.innerHTML = `
            <div class="text-center py-12 text-gray-400">
                <p>No files yet. Upload documents to get started.</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = files.map(file => {
        // Extract filename from path if needed, usually backend returns path relative to KB root?
        // Assuming backend returns filenames or relative paths
        const filename = file.split('/').pop(); 
        
        return `
        <div class="file-item p-4 flex justify-between items-center hover:bg-gray-50 group">
            <div class="flex items-center gap-3">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                <span class="text-gray-700">${filename}</span>
            </div>
            <button onclick="deleteFile('${filename}')" class="text-gray-400 hover:text-error opacity-0 group-hover:opacity-100 transition-all p-1">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
            </button>
        </div>
    `}).join('');
}

async function deleteFile(filename) {
    if (!confirm(`Are you sure you want to delete "${filename}"?`)) return;
    
    try {
        await apiCall(`/instructor/kbs/${selectedKb}/files/${filename}`, {
            method: 'DELETE'
        });
        showNotification('File deleted', 'success');
        loadKbDetails(selectedKb);
    } catch (error) {
        showNotification('Error deleting file: ' + error.message, 'error');
    }
}

function setupDragAndDrop(kbName) {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-upload');
    
    // Prevent default behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });
    
    // Highlight drop zone
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });
    
    // Handle drop
    dropZone.addEventListener('drop', handleDrop, false);
    
    // Handle click
    dropZone.onclick = () => fileInput.click();
    fileInput.onchange = (e) => handleFiles(e.target.files);
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    function highlight(e) {
        dropZone.classList.add('drag-active');
    }
    
    function unhighlight(e) {
        dropZone.classList.remove('drag-active');
    }
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }
    
    async function handleFiles(files) {
        const validFiles = [...files].filter(file => 
            file.name.endsWith('.txt') || file.name.endsWith('.md') || file.name.endsWith('.pdf')
        );
        
        if (validFiles.length === 0) {
            showNotification('Only .txt, .md, and .pdf files are supported', 'error');
            return;
        }

        const statusContainer = document.getElementById('kb-existing-upload-status');
        const statusList = document.getElementById('kb-existing-upload-list');
        statusContainer.classList.remove('hidden');

        // Helper
        const getFormattedSize = (file) => {
            const sizeKB = file.size / 1024;
            if (sizeKB < 1000) return `(${sizeKB.toFixed(1)} KB)`;
            return `(${(sizeKB/1024).toFixed(2)} MB)`; 
        };

        // Reset list for new batch
        statusList.innerHTML = validFiles.map((f, i) => `
            <div id="ex-upload-item-${i}" class="p-2 flex items-center justify-between">
                <div class="flex items-center gap-2 truncate pr-2">
                     <span class="font-medium text-gray-700">${f.name}</span>
                     <span class="text-xs text-gray-400">${getFormattedSize(f)}</span>
                </div>
                <span class="status-icon text-gray-400 text-xs">Pending...</span>
            </div>
        `).join('');
        
        let successCount = 0;
        const failedFilenames = [];
        
        for (let i = 0; i < validFiles.length; i++) {
            const file = validFiles[i];
            const row = document.getElementById(`ex-upload-item-${i}`);
            const statusEl = row.querySelector('.status-icon');

            // Check size (2MB)
            if (file.size > 2 * 1024 * 1024) {
                 statusEl.innerHTML = '<span class="text-error font-bold text-xs">Too Large (>2MB)</span>';
                 row.classList.add('bg-red-50');
                 failedFilenames.push(`${file.name} (Too Large)`);
                 continue;
            }

            try {
                statusEl.innerHTML = '<span class="animate-spin inline-block w-3 h-3 border-2 border-primary border-t-transparent rounded-full"></span>';
                
                await uploadFileToKb(kbName, file);
                
                statusEl.innerHTML = '<span class="text-green-600 font-bold">✓</span>';
                row.classList.add('bg-green-50');
                successCount++;
                
            } catch (error) {
                console.error(`Error uploading ${file.name}:`, error);
                statusEl.innerHTML = '<span class="text-red-500 font-bold">✗</span>';
                row.classList.add('bg-red-50');
                failedFilenames.push(file.name);
            }
        }

        // Final refresh
        await loadKbDetails(kbName);

        // Show summary modal
        showUploadSummaryModal(validFiles.length, successCount, failedFilenames, () => {
            // Context closed callback
            statusContainer.classList.add('hidden');
        });
    }
}


// ============================================================================
// Class Management & Account Settings
// ============================================================================

let currentRosterClassId = null;

async function loadClasses() {
    try {
        const container = document.getElementById('classes-list');
        const selector = document.getElementById('active-class-selector');
        
        container.innerHTML = '';
        selector.innerHTML = '';
        
        enrolledClasses = await apiCall('/classes');
        
        if (enrolledClasses.length === 0) {
            selector.classList.add('hidden');
            container.innerHTML = `
                <div class="col-span-full text-center py-12 text-gray-500 bg-gray-50 rounded-xl border-2 border-dashed border-gray-200">
                    <h3 class="text-xl text-gray-800 font-bold mb-2">Welcome to ChiPT!</h3>
                    <p>You haven't joined any classes yet. Create or Join a class above to get started.</p>
                </div>
            `;
            currentClassId = null;
            
            // Redirect straight to settings if they have no classes
            showAccountSettingsView();
            
        } else {
            selector.classList.remove('hidden');
            let foundCurrent = false;

            // Hide empty state if classes exist
            const emptyState = document.getElementById('dashboard-empty-state');
            const contentLayer = document.getElementById('dashboard-content-layer');
            if (emptyState) emptyState.classList.add('hidden');
            if (contentLayer) contentLayer.classList.remove('hidden');
            
            // Default to the first class if none selected
            if (!currentClassId && enrolledClasses.length > 0) {
                currentClassId = enrolledClasses[0].id;
            }
            
            enrolledClasses.forEach(c => {
                // Dropdown setup
                const option = document.createElement('option');
                option.value = c.id;
                option.textContent = c.name;
                selector.appendChild(option);
                
                if (c.id == currentClassId) foundCurrent = true;

                // Card setup
                const card = document.createElement('div');
                card.className = "bg-white border rounded-xl p-5 hover:shadow-md transition-shadow cursor-pointer flex flex-col h-full";
                const isInstructor = c.role === 'instructor' || c.role === 'owner';
                
                card.innerHTML = `
                    <div class="flex justify-between items-start mb-2">
                        <h3 class="text-xl font-bold font-serif text-gray-800 break-words flex-1 pr-2">${c.name}</h3>
                        <div class="flex items-center gap-2">
                            ${c.role === 'owner' || currentUser.role === 'admin' ? `
                            <button onclick="event.stopPropagation(); deleteClass(${c.id}, '${c.name.replace(/'/g, "\\'")}')" class="text-gray-400 hover:text-red-500 transition-colors" title="Delete Class">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                            </button>
                            ` : ''}
                            <span class="px-2 py-1 bg-gray-100 text-xs font-semibold rounded ${isInstructor ? 'text-purple-700' : 'text-gray-600'}">
                                ${c.role.toUpperCase()}
                            </span>
                        </div>
                    </div>
                    ${isInstructor ? `
                    <div class="mt-2 mb-4 bg-gray-50 p-3 rounded-lg border border-gray-200">
                        <div class="flex justify-between items-center mb-1">
                            <span class="text-xs font-semibold text-gray-500 uppercase">Join Code</span>
                            <button onclick="event.stopPropagation(); rotateClassCode(${c.id})" class="text-xs text-primary hover:text-primary-dark font-medium flex items-center gap-1 transition-colors">
                                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                                Rotate
                            </button>
                        </div>
                        <div class="font-mono text-center text-sm font-bold text-gray-800 bg-white px-2 py-1 rounded border border-gray-300">
                            <span id="join-code-display-${c.id}">${c.code || 'Hidden'}</span>
                        </div>
                    </div>
                    ` : ''}
                    <div class="mt-auto pt-4 flex gap-2">
                        ${isInstructor ? `
                        <button onclick="event.stopPropagation(); openTAModal(${c.id}, '${c.name.replace(/'/g, "\\'")}')" class="btn-secondary text-sm px-3 py-1 flex-1 border border-primary text-primary hover:bg-primary-50">
                            Manage TAs
                        </button>
                        <button onclick="event.stopPropagation(); openRosterModal(${c.id}, '${c.name.replace(/'/g, "\\'")}', '${c.role}')" class="btn-primary text-sm px-3 py-1 flex-1 border border-primary">
                            Roster
                        </button>
                        ` : `
                        <button onclick="event.stopPropagation(); document.getElementById('active-class-selector').value = '${c.id}'; switchActiveClass(); showDashboardView();" class="btn-secondary text-sm px-3 py-1 flex-1">
                            Q&A
                        </button>
                        `}
                    </div>
                `;
                container.appendChild(card);
            });
        }
        
        if (currentUser.role === 'instructor' || currentUser.role === 'admin') {
            document.getElementById('create-class-btn').classList.remove('hidden');
            document.getElementById('create-class-btn').classList.add('flex');
        } else {
            document.getElementById('create-class-btn').classList.add('hidden');
            document.getElementById('create-class-btn').classList.remove('flex');
        }

    } catch (error) {
        showNotification('Failed to load classes: ' + error.message, 'error');
    }
}

async function switchActiveClass() {
    const selector = document.getElementById('active-class-selector');
    if (!selector.value) return;
    
    currentClassId = parseInt(selector.value);
    
    if (document.getElementById('dashboard-view').classList.contains('hidden') &&
        document.getElementById('kb-view').classList.contains('hidden')) {
        // If they are in settings, maybe don't force a swap, just load questions in background.
        await loadQuestions();
    } else {
        // Force refresh of the current view
        if (!document.getElementById('dashboard-view').classList.contains('hidden')) {
            await loadQuestions();
        } else if (!document.getElementById('kb-view').classList.contains('hidden')) {
            await loadKnowledgeBases();
        }
    }
}

// Join Class Modal
function showJoinClassModal() {
    document.getElementById('join-class-code').value = '';
    document.getElementById('join-class-modal').classList.remove('hidden');
}

function closeJoinClassModal() {
    document.getElementById('join-class-modal').classList.add('hidden');
}

document.getElementById('join-class-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const code = document.getElementById('join-class-code').value;
    try {
        showLoading();
        const res = await apiCall('/classes/join', {
            method: 'POST',
            body: JSON.stringify({ code })
        });
        showNotification(res.message, 'success');
        
        if (res.class_id) {
            currentClassId = res.class_id;
        }
        
        closeJoinClassModal();
        loadClasses();
    } catch (error) {
        showNotification('Error joining class: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
});

// Create Class Modal
function showCreateClassModal() {
    document.getElementById('create-class-name').value = '';
    document.getElementById('create-class-success').classList.add('hidden');
    document.getElementById('create-class-form').classList.remove('hidden');
    document.getElementById('create-class-modal').classList.remove('hidden');
}

function closeCreateClassModal() {
    document.getElementById('create-class-modal').classList.add('hidden');
}

document.getElementById('create-class-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('create-class-name').value;
    try {
        showLoading();
        const res = await apiCall('/classes', {
            method: 'POST',
            body: JSON.stringify({ name })
        });
        
        // Show success context
        document.getElementById('create-class-form').classList.add('hidden');
        const successDiv = document.getElementById('create-class-success');
        successDiv.classList.remove('hidden');
        document.getElementById('new-class-join-code').textContent = res.code;
        
        if (res.id) {
            currentClassId = res.id;
        }
        
        loadClasses();
    } catch (error) {
        showNotification('Error creating class: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
});

async function deleteClass(classId, className) {
    if (!confirm(`Are you absolutely sure you want to delete the class "${className}"? This action cannot be undone and will delete all enrollments and related data.`)) {
        return;
    }
    
    try {
        showLoading();
        const res = await apiCall(`/classes/${classId}`, {
            method: 'DELETE'
        });
        showNotification(res.message, 'success');
        loadClasses();
    } catch (error) {
        showNotification('Error deleting class: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function openRosterModal(classId, className, currentRole) {
    currentRosterClassId = classId;
    document.getElementById('roster-modal').classList.remove('hidden');
    document.getElementById('roster-modal-title').textContent = `Roster: ${className}`;
    
    // Display join code
    const targetClass = enrolledClasses.find(c => c.id == classId);
    if (targetClass) {
        document.getElementById('current-join-code-span').textContent = targetClass.code || 'Hidden';
    }
    
    const actionsEl = document.getElementById('roster-actions');
    const isStaff = currentRole === 'instructor' || currentRole === 'owner';
    if (isStaff) {
        actionsEl.classList.remove('hidden');
    } else {
        actionsEl.classList.add('hidden');
    }
    
    await loadRoster(classId, currentRole);
}

function closeRosterModal() {
    document.getElementById('roster-modal').classList.add('hidden');
    currentRosterClassId = null;
}

// TA Management Modal Logic
async function openTAModal(classId, className) {
    currentRosterClassId = classId;
    document.getElementById('ta-modal').classList.remove('hidden');
    document.getElementById('ta-modal-title').textContent = `Manage TAs: ${className}`;
    await loadTAs(classId);
}

function closeTAModal() {
    document.getElementById('ta-modal').classList.add('hidden');
    document.getElementById('new-ta-email').value = '';
}

document.getElementById('add-ta-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!currentRosterClassId) return;
    
    const email = document.getElementById('new-ta-email').value;
    try {
        await apiCall(`/classes/${currentRosterClassId}/tas`, {
            method: 'POST',
            body: JSON.stringify({ email })
        });
        showNotification('TA added successfully', 'success');
        document.getElementById('new-ta-email').value = '';
        await loadTAs(currentRosterClassId);
    } catch (error) {
        showNotification('Error adding TA: ' + error.message, 'error');
    }
});

async function loadTAs(classId) {
    const tbody = document.getElementById('ta-table-body');
    const loading = document.getElementById('ta-loading');
    
    tbody.innerHTML = '';
    loading.classList.remove('hidden');
    
    try {
        const res = await apiCall(`/classes/${classId}/tas`);
        loading.classList.add('hidden');
        
        if (res.tas.length === 0) {
            tbody.innerHTML = `<tr><td colspan="2" class="text-center py-4 text-gray-500">No pre-approved TAs</td></tr>`;
            return;
        }
        
        res.tas.forEach(ta => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="px-4 py-3 border-b">${ta.email}</td>
                <td class="px-4 py-3 border-b text-right flex justify-end">
                    <button onclick="removeTA('${ta.email}')" class="text-error hover:text-red-700 bg-red-50 hover:bg-red-100 p-1.5 rounded transition-colors" title="Remove TA">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        loading.classList.add('hidden');
        tbody.innerHTML = `<tr><td colspan="2" class="text-center py-4 text-error">${error.message}</td></tr>`;
    }
}

async function removeTA(email) {
    if (!currentRosterClassId) return;
    if (!confirm(`Are you sure you want to remove ${email} from the TA allowlist?`)) return;
    
    try {
        await apiCall(`/classes/${currentRosterClassId}/tas/${encodeURIComponent(email)}`, {
            method: 'DELETE'
        });
        showNotification('TA removed', 'success');
        await loadTAs(currentRosterClassId);
    } catch (error) {
        showNotification('Error removing TA: ' + error.message, 'error');
    }
}

let currentRosterData = [];
let currentRosterRole = null;
let currentSortCol = 'name';
let currentSortDesc = false;

async function loadRoster(classId, currentRole) {
    const tbody = document.getElementById('roster-table-body');
    const loading = document.getElementById('roster-loading');
    
    tbody.innerHTML = '';
    loading.classList.remove('hidden');
    
    try {
        const res = await apiCall(`/classes/${classId}/roster`);
        currentRosterData = res.roster;
        currentRosterRole = currentRole;
        
        loading.classList.add('hidden');
        renderRosterList();
        
    } catch (error) {
        loading.classList.add('hidden');
        tbody.innerHTML = `<tr><td colspan="4" class="text-center py-4 text-error">${error.message}</td></tr>`;
    }
}

function sortRoster(col) {
    if (currentSortCol === col) {
        currentSortDesc = !currentSortDesc;
    } else {
        currentSortCol = col;
        currentSortDesc = false;
    }
    renderRosterList();
}

function renderRosterList() {
    const tbody = document.getElementById('roster-table-body');
    const searchTerm = document.getElementById('roster-search')?.value.toLowerCase() || '';
    
    // Reset sort icons
    document.getElementById('sort-icon-name').textContent = '';
    document.getElementById('sort-icon-email').textContent = '';
    document.getElementById('sort-icon-role').textContent = '';
    
    const iconEl = document.getElementById(`sort-icon-${currentSortCol}`);
    if (iconEl) {
        iconEl.textContent = currentSortDesc ? '▼' : '▲';
    }
    
    let filtered = currentRosterData;
    if (searchTerm) {
        filtered = currentRosterData.filter(u => 
            (u.full_name && u.full_name.toLowerCase().includes(searchTerm)) ||
            (u.email && u.email.toLowerCase().includes(searchTerm))
        );
    }
    
    filtered.sort((a, b) => {
        let valA = a[currentSortCol === 'name' ? 'full_name' : currentSortCol] || '';
        let valB = b[currentSortCol === 'name' ? 'full_name' : currentSortCol] || '';
        
        if (currentSortCol === 'role') {
            valA = a.class_role || '';
            valB = b.class_role || '';
        }
        
        valA = valA.toLowerCase();
        valB = valB.toLowerCase();
        
        if (valA < valB) return currentSortDesc ? 1 : -1;
        if (valA > valB) return currentSortDesc ? -1 : 1;
        return 0;
    });
    
    tbody.innerHTML = '';
    
    if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" class="text-center py-4 text-gray-500">No users found</td></tr>`;
        return;
    }
    
    filtered.forEach(user => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="px-4 py-3 border-b">${user.full_name || 'N/A'}</td>
            <td class="px-4 py-3 border-b">${user.email}</td>
            <td class="px-4 py-3 border-b">
                <span class="px-2 py-1 rounded text-xs font-semibold 
                    ${user.class_role === 'owner' ? 'bg-amber-100 text-amber-800' :
                      user.class_role === 'instructor' ? 'bg-purple-100 text-purple-800' : 
                      user.class_role === 'ta' ? 'bg-blue-100 text-blue-800' : 
                      'bg-gray-100 text-gray-800'}">
                    ${user.class_role.toUpperCase()}
                </span>
            </td>
            <td class="px-4 py-3 border-b text-right">
                ${(currentRosterRole === 'owner' || currentRosterRole === 'instructor') && user.class_role !== 'owner' ? `
                    <select onchange="setClassRole(${user.user_id}, this.value)" class="text-sm border rounded px-2 py-1 bg-white focus:ring-1 focus:ring-primary focus:border-primary" ${currentRosterRole === 'instructor' && user.class_role === 'instructor' ? 'disabled' : ''}>
                        <option value="student" ${user.class_role === 'student' ? 'selected' : ''}>Student</option>
                        <option value="ta" ${user.class_role === 'ta' ? 'selected' : ''}>TA</option>
                        ${currentRosterRole === 'owner' || currentUser.role === 'admin' ? `<option value="instructor" ${user.class_role === 'instructor' ? 'selected' : ''}>Instructor</option>` : ''}
                    </select>
                ` : ''}
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function setClassRole(userId, newRole) {
    if (!currentRosterClassId) return;
    try {
        await apiCall(`/classes/${currentRosterClassId}/set-role`, {
            method: 'POST',
            body: JSON.stringify({ user_id: userId, class_role: newRole })
        });
        showNotification('Role updated successfully', 'success');
        // Reload roster to reflect changes
        loadRoster(currentRosterClassId, true);
    } catch (error) {
        showNotification('Failed to update role: ' + error.message, 'error');
        // Reload to revert select element if it failed
        loadRoster(currentRosterClassId, true);
    }
}

async function rotateClassCode(classId = null) {
    const targetId = classId || currentRosterClassId;
    if (!targetId) return;
    if (!confirm("Are you sure you want to rotate the join code? The old code will immediately stop working.")) return;
    
    try {
        const res = await apiCall(`/classes/${targetId}/rotate-code`, {
            method: 'POST'
        });
        
        const displaySpan = document.getElementById(`join-code-display-${targetId}`);
        if (displaySpan) displaySpan.textContent = res.join_code;
        
        const currentModalSpan = document.getElementById('current-join-code-span');
        if (currentModalSpan) currentModalSpan.textContent = res.join_code;
        
        alert(`New Join Code generated!\n\nJOIN CODE: ${res.join_code}\n\nWARNING: Copy this now. It will not be shown again.`);
    } catch (error) {
        showNotification('Failed to rotate code: ' + error.message, 'error');
    }
}


document.getElementById('update-email-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const errorEl = document.getElementById('update-email-error');
    errorEl.classList.add('hidden');
    
    const new_email = document.getElementById('update-new-email').value;
    const password = document.getElementById('update-email-password').value;
    
    if (!new_email.toLowerCase().endsWith('@purdue.edu')) {
        errorEl.textContent = 'Email must be a @purdue.edu address';
        errorEl.classList.remove('hidden');
        return;
    }
    
    try {
        showLoading();
        const res = await apiCall('/account/update-email', {
            method: 'POST',
            body: JSON.stringify({ new_email, password })
        });
        
        // On success, the token is invalidated, we must force logout and show verify view.
        clearToken();
        disconnectWebSocket();
        showAuthView();
        
        document.getElementById('update-new-email').value = '';
        document.getElementById('update-email-password').value = '';
        
        alert("Email update initiated! " + res.message);
        
    } catch (error) {
        errorEl.textContent = error.message;
        errorEl.classList.remove('hidden');
    } finally {
        hideLoading();
    }
});


// ============================================================================
// Event Listeners
// ============================================================================

document.getElementById('show-login').addEventListener('click', () => {
    document.getElementById('login-form').classList.remove('hidden');
    document.getElementById('register-form').classList.add('hidden');
    document.getElementById('show-login').classList.add('bg-white', 'text-primary', 'shadow-sm');
    document.getElementById('show-login').classList.remove('text-gray-600');
    document.getElementById('show-register').classList.remove('bg-white', 'text-primary', 'shadow-sm');
    document.getElementById('show-register').classList.add('text-gray-600');
    hideError('login-error');
    hideError('register-error');
});

document.getElementById('show-register').addEventListener('click', () => {
    document.getElementById('register-form').classList.remove('hidden');
    document.getElementById('login-form').classList.add('hidden');
    document.getElementById('show-register').classList.add('bg-white', 'text-primary', 'shadow-sm');
    document.getElementById('show-register').classList.remove('text-gray-600');
    document.getElementById('show-login').classList.remove('bg-white', 'text-primary', 'shadow-sm');
    document.getElementById('show-login').classList.add('text-gray-600');
    hideError('login-error');
    hideError('register-error');
});

document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    hideError('login-error');
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    try {
        showLoading();
        const data = await apiCall('/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        
        setToken(data.access_token);
        await loadCurrentUser();
    } catch (error) {
        showError('login-error', error.message);
    } finally {
        hideLoading();
    }
});

document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    hideError('register-error');
    
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const intent = document.getElementById('register-role').value;
    
    if (!email.toLowerCase().endsWith('@purdue.edu')) {
        showError('register-error', 'Email must be a @purdue.edu address');
        return;
    }
    
    try {
        showLoading();
        const res = await apiCall('/register', {
            method: 'POST',
            body: JSON.stringify({ email, password, intent })
        });
        
        document.getElementById('register-form').classList.add('hidden');
        if (res.requires_verification === false) {
            const loginRes = await apiCall('/login', {
                method: 'POST',
                body: JSON.stringify({ email, password })
            });
            setToken(loginRes.access_token);
            await loadCurrentUser();
        } else {
            document.getElementById('register-success-view').classList.remove('hidden');
        }
    } catch (error) {
        showError('register-error', error.message);
    } finally {
        hideLoading();
    }
});

document.getElementById('show-login-from-success')?.addEventListener('click', () => {
    document.getElementById('show-login').click();
    document.getElementById('register-success-view').classList.add('hidden');
    document.getElementById('login-form').classList.remove('hidden');
});

document.getElementById('logout-btn').addEventListener('click', () => {
    clearToken();
    currentUser = null;
    selectedQuestionId = null;
    allQuestions = [];
    disconnectWebSocket();
    showAuthView();
    
    document.getElementById('login-email').value = '';
    document.getElementById('login-password').value = '';
    document.getElementById('register-email').value = '';
    document.getElementById('register-password').value = '';
});

document.getElementById('new-question-btn').addEventListener('click', showNewQuestionModal);

document.getElementById('search-questions')?.addEventListener('input', (e) => {
    renderQuestionsSidebar(allQuestions);
});

// ============================================================================
// Initialize
// ============================================================================

async function init() {
    const urlParams = new URLSearchParams(window.location.search);
    const verifyToken = urlParams.get('token');
    const verifyEmail = urlParams.get('email');
    
    if (verifyToken && verifyEmail) {
        document.getElementById('auth-view').classList.add('hidden');
        document.getElementById('verify-view').classList.remove('hidden');
        
        try {
            await apiCall('/verify-email', {
                method: 'POST',
                body: JSON.stringify({ email: verifyEmail, token: verifyToken })
            });
            
            document.getElementById('verify-loading').classList.add('hidden');
            document.getElementById('verify-success').classList.remove('hidden');
        } catch (error) {
            document.getElementById('verify-loading').classList.add('hidden');
            document.getElementById('verify-error').classList.remove('hidden');
            document.getElementById('verify-error-msg').textContent = error.message;
        }
        return;
    }
    
    if (getToken()) {
        loadCurrentUser();
    } else {
        showAuthView();
    }
}

init();

function showUploadSummaryModal(total, success, failedFiles, onContextClose) {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    
    const failedListHtml = failedFiles.length > 0 ? `
        <div class="mt-4">
            <h4 class="font-bold text-error mb-2">Failed Files (${failedFiles.length})</h4>
            <div class="bg-red-50 border border-red-100 rounded-lg p-3 max-h-40 overflow-y-auto">
                <ul class="text-sm text-red-700 space-y-1">
                    ${failedFiles.map(f => `<li>• ${f}</li>`).join('')}
                </ul>
            </div>
        </div>
    ` : '';
    
    modal.innerHTML = `
        <div class="modal-content">
            <h3 class="text-2xl font-bold serif mb-4">Upload Summary</h3>
            
            <div class="flex items-center gap-4 mb-4">
                <div class="flex-1 bg-gray-100 rounded-lg p-4 text-center">
                    <p class="text-gray-500 text-xs uppercase font-bold">Total</p>
                    <p class="text-2xl font-bold text-gray-800">${total}</p>
                </div>
                <div class="flex-1 bg-green-50 rounded-lg p-4 text-center">
                    <p class="text-green-600 text-xs uppercase font-bold">Success</p>
                    <p class="text-2xl font-bold text-green-700">${success}</p>
                </div>
                <div class="flex-1 bg-red-50 rounded-lg p-4 text-center">
                    <p class="text-red-600 text-xs uppercase font-bold">Failed</p>
                    <p class="text-2xl font-bold text-red-700">${failedFiles.length}</p>
                </div>
            </div>
            
            ${failedListHtml}
            
            <div class="mt-6 flex justify-end">
                <button class="btn-primary" id="summary-close-btn">
                    Close & View Files
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    document.getElementById('summary-close-btn').onclick = () => {
        modal.remove();
        if (onContextClose) onContextClose();
    };
}
