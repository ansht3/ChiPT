let currentUser = null;
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
    // Parse markdown
    let html = marked.parse(content);
    
    // Create temp element for math rendering
    const temp = document.createElement('div');
    temp.innerHTML = html;
    
    // Render math equations
    renderMathInElement(temp, {
        delimiters: [
            {left: '$$', right: '$$', display: true},
            {left: '$', right: '$', display: false},
            {left: '\\[', right: '\\]', display: true},
            {left: '\\(', right: '\\)', display: false}
        ],
        throwOnError: false
    });
    
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
            throw new Error('Session expired. Please login again.');
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
// View Management
// ============================================================================

function showAuthView() {
    document.getElementById('auth-view').classList.remove('hidden');
    document.getElementById('dashboard-view').classList.add('hidden');
    document.getElementById('nav-actions').classList.add('hidden');
    disconnectWebSocket();
}

function showDashboardView() {
    document.getElementById('auth-view').classList.add('hidden');
    document.getElementById('dashboard-view').classList.remove('hidden');
    document.getElementById('kb-view').classList.add('hidden');
    document.getElementById('nav-actions').classList.remove('hidden');
    document.getElementById('nav-actions').classList.add('flex');
}

function showKbView() {
    document.getElementById('auth-view').classList.add('hidden');
    document.getElementById('dashboard-view').classList.add('hidden');
    document.getElementById('kb-view').classList.remove('hidden');
    document.getElementById('nav-actions').classList.remove('hidden');
    document.getElementById('nav-actions').classList.add('flex');
    loadKnowledgeBases();
    fetchActiveKb();
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
            ${currentUser.role === 'instructor' ? `
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
    
    const isInstructor = currentUser.role === 'instructor';
    const messages = question.messages || [];
    
    container.innerHTML = `
        <div class="max-w-3xl mx-auto animate-slide-in">
            <!-- Question Header -->
            <div class="bg-white rounded-2xl shadow-lg p-6 mb-6">
                <div class="flex items-start justify-between gap-4 mb-4">
                    <div class="flex-1">
                        ${isInstructor ? `
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
                    <div class="text-gray-800 leading-relaxed">${escapeHtml(question.content)}</div>
                </div>
            </div>
            
            <!-- Chat Thread -->
            <div class="bg-white rounded-2xl shadow-lg p-6 mb-6">
                <h3 class="text-lg font-bold serif text-gray-900 mb-4">Conversation</h3>
                
                <div class="chat-thread mb-6">
                    ${messages.length === 0 ? `
                        <div class="text-center py-8 text-gray-400">
                            <p class="text-sm">No messages yet. ${isInstructor ? 'Be the first to respond!' : 'Waiting for instructor response...'}</p>
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
                
                ${isInstructor ? `
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

                        <div id="kb-selection-${question.id}" class="mb-4 ${currentUser.role === 'instructor' ? '' : 'hidden'}">
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
    if (isInstructor) {
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
        
        await apiCall(`/questions/${questionId}/messages`, {
            method: 'POST',
            body: JSON.stringify({
                content: content,
                source: currentUser.role === 'instructor' ? source : null
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
        showLoading();
        
        if (currentUser.role === 'student') {
            allQuestions = await apiCall('/questions');
        } else {
            allQuestions = await apiCall('/instructor/questions');
        }
        
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
        
        if (currentUser.role === 'instructor') {
            document.getElementById('kb-btn').classList.remove('hidden');
            document.getElementById('kb-btn').classList.add('flex');
            document.getElementById('kb-btn').onclick = showKbView;
        } else {
            document.getElementById('kb-btn').classList.add('hidden');
            document.getElementById('kb-btn').classList.remove('flex');
        }

        showDashboardView();
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
        
        if (!content) {
            errorEl.textContent = 'Question cannot be empty';
            errorEl.classList.remove('hidden');
            return;
        }
        
        try {
            showLoading();
            await apiCall('/questions', {
                method: 'POST',
                body: JSON.stringify({ content })
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
                        <input type="file" id="create-kb-files" multiple accept=".txt,.md" class="hidden">
                        <svg class="w-8 h-8 text-gray-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                        </svg>
                        <p class="text-sm text-gray-600 font-medium">Click to select files</p>
                        <p class="text-xs text-gray-500">.txt or .md</p>
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
        const data = await apiCall('/instructor/kbs');
        allKbs = data.kbs || [];
        renderKbList(allKbs);
    } catch (error) {
        showNotification('Failed to load KBs: ' + error.message, 'error');
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
            file.name.endsWith('.txt') || file.name.endsWith('.md')
        );
        
        if (validFiles.length === 0) {
            showNotification('Only .txt and .md files are supported', 'error');
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
    
    try {
        showLoading();
        await apiCall('/register', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        
        const loginData = await apiCall('/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        
        setToken(loginData.access_token);
        await loadCurrentUser();
    } catch (error) {
        showError('register-error', error.message);
    } finally {
        hideLoading();
    }
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

if (getToken()) {
    loadCurrentUser();
} else {
    showAuthView();
}

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
