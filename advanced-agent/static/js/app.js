// Modern Multi Agent Researcher UI - Perplexity Style

class ModernResearchAgent {
    constructor() {
        this.currentResearch = null;
        this.selectedPdfs = [];
        this.currentQuery = '';
        this.init();
    }

    init() {
        this.bindEvents();
        this.checkStatus();
        this.setupAutoResize();
        this.initDarkMode();
    }

    bindEvents() {
        // Dark mode toggle
        document.getElementById('dark-mode-btn').addEventListener('click', () => {
            this.toggleDarkMode();
        });

        // Search functionality
        document.getElementById('research-btn').addEventListener('click', () => {
            this.startResearch();
        });

        // Auto-resize textarea
        const textarea = document.getElementById('query');
        textarea.addEventListener('input', (e) => {
            this.autoResize(e.target);
            this.currentQuery = e.target.value.trim();
        });

        // Enter key to search
        textarea.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.startResearch();
            }
        });

        // Research mode changes
        document.querySelectorAll('input[name="research-mode"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.handleModeChange(e.target.value);
            });
        });

        // Suggestion chips
        document.querySelectorAll('.suggestion-chip').forEach(chip => {
            chip.addEventListener('click', (e) => {
                const query = e.currentTarget.dataset.query;
                document.getElementById('query').value = query;
                this.currentQuery = query;
                this.autoResize(document.getElementById('query'));
            });
        });

        // New search button
        document.getElementById('new-search-btn').addEventListener('click', () => {
            this.startNewSearch();
        });

        // Export and share buttons
        document.getElementById('export-btn').addEventListener('click', () => {
            this.exportResults();
        });

        document.getElementById('share-btn').addEventListener('click', () => {
            this.shareResults();
        });

        // Retry button
        document.getElementById('retry-btn').addEventListener('click', () => {
            this.startResearch();
        });
    }

    setupAutoResize() {
        const textarea = document.getElementById('query');
        this.autoResize(textarea);
    }

    autoResize(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }

    async checkStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            const statusIndicator = document.getElementById('status-indicator');
            const statusDot = statusIndicator.querySelector('.status-dot');
            const statusText = statusIndicator.querySelector('span');
            
            if (data.workflow_ready) {
                statusDot.style.background = 'var(--success-color)';
                statusText.textContent = 'Ready';
            } else {
                statusDot.style.background = 'var(--error-color)';
                statusText.textContent = 'Error';
                this.showError('Research agent is not ready. Please check the configuration.');
                document.getElementById('research-btn').disabled = true;
            }
        } catch (error) {
            console.error('Error checking status:', error);
        }
    }

    async handleModeChange(mode) {
        const pdfPanel = document.getElementById('pdf-panel');
        
        if (mode === 'select_pdfs') {
            pdfPanel.style.display = 'block';
            await this.loadAllPdfs();
        } else if (mode === 'relevant_pdfs') {
            pdfPanel.style.display = 'block';
            if (this.currentQuery) {
                await this.loadRelevantPdfs(this.currentQuery);
            } else {
                document.getElementById('pdf-list').innerHTML = 
                    '<div class="empty-state">Enter a query to see relevant documents</div>';
            }
        } else {
            pdfPanel.style.display = 'none';
        }
    }

    async loadAllPdfs() {
        try {
            const response = await fetch('/api/pdfs');
            const data = await response.json();
            
            if (data.success) {
                this.renderPdfList(data.pdfs, false);
            } else {
                document.getElementById('pdf-list').innerHTML = 
                    `<div class="error-state">Error loading PDFs: ${data.error}</div>`;
            }
        } catch (error) {
            document.getElementById('pdf-list').innerHTML = 
                `<div class="error-state">Error loading PDFs: ${error.message}</div>`;
        }
    }

    async loadRelevantPdfs(query) {
        try {
            const response = await fetch('/api/relevant-pdfs', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.renderPdfList(data.pdfs, true);
            } else {
                document.getElementById('pdf-list').innerHTML = 
                    `<div class="error-state">Error loading relevant PDFs: ${data.error}</div>`;
            }
        } catch (error) {
            document.getElementById('pdf-list').innerHTML = 
                `<div class="error-state">Error loading relevant PDFs: ${error.message}</div>`;
        }
    }

    renderPdfList(pdfs, showRelevance = false) {
        const pdfList = document.getElementById('pdf-list');
        
        if (!pdfs || pdfs.length === 0) {
            pdfList.innerHTML = '<div class="empty-state">No documents available</div>';
            return;
        }

        const html = pdfs.map(pdf => {
            const relevanceScore = pdf.relevance_score || 0;
            const relevanceWidth = Math.round(relevanceScore * 100);
            
            return `
                <div class="pdf-item">
                    <input type="checkbox" id="pdf-${pdf.s3_key}" value="${pdf.s3_key}">
                    <div class="pdf-info">
                        <div class="pdf-name">${pdf.filename}</div>
                        <div class="pdf-details">
                            ${pdf.size_mb ? `${pdf.size_mb} MB` : ''} 
                            ${pdf.last_modified ? `• ${new Date(pdf.last_modified).toLocaleDateString()}` : ''}
                            ${pdf.summary ? `<br>${pdf.summary.substring(0, 80)}...` : ''}
                        </div>
                    </div>
                    ${showRelevance ? `
                        <div class="pdf-relevance">
                            <span>${relevanceScore.toFixed(2)}</span>
                            <div class="relevance-bar">
                                <div class="relevance-fill" style="width: ${relevanceWidth}%"></div>
                            </div>
                        </div>
                    ` : ''}
                </div>
            `;
        }).join('');

        pdfList.innerHTML = html;

        // Add event listeners to checkboxes
        pdfList.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                if (e.target.checked) {
                    this.selectedPdfs.push(e.target.value);
                } else {
                    this.selectedPdfs = this.selectedPdfs.filter(pdf => pdf !== e.target.value);
                }
            });
        });
    }

    async startResearch() {
        const query = document.getElementById('query').value.trim();
        const mode = document.querySelector('input[name="research-mode"]:checked').value;

        if (!query) {
            this.showError('Please enter a research query');
            return;
        }

        // Hide search interface and show loading
        this.showLoading();
        this.startLiveProgress(query, mode);
    }

    startLiveProgress(query, mode) {
        // Show live progress
        document.querySelector('.progress-feed').style.display = 'block';
        
        const progressList = document.getElementById('progress-list');
        progressList.innerHTML = '';

        try {
            // Use EventSource for real-time updates
            const eventSource = new EventSource('/api/research-stream?' + new URLSearchParams({
                query: query,
                mode: mode,
                selected_pdfs: JSON.stringify(this.selectedPdfs)
            }));

            eventSource.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleProgressUpdate(data);
                    
                    if (data.status === 'completed') {
                        eventSource.close();
                        this.showResults(data.result, { query: query });
                        this.addToHistory(query);
                    } else if (data.status === 'error') {
                        eventSource.close();
                        this.showError(data.message);
                    }
                } catch (e) {
                    console.error('Error parsing SSE data:', e);
                }
            };

            eventSource.onerror = (error) => {
                console.error('SSE Error:', error);
                eventSource.close();
                // Fallback to regular API
                this.fallbackToRegularAPI(query, mode);
            };

        } catch (error) {
            console.error('Error starting live progress:', error);
            this.fallbackToRegularAPI(query, mode);
        }
    }

    async fallbackToRegularAPI(query, mode) {
        try {
            const requestData = {
                query: query,
                mode: mode,
                selected_pdfs: this.selectedPdfs
            };

            const response = await fetch('/api/research', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestData)
            });

            const data = await response.json();

            if (data.success) {
                this.showResults(data.result, data.research_info);
                this.addToHistory(query);
            } else {
                this.showError(data.error);
            }
        } catch (error) {
            this.showError(`Network error: ${error.message}`);
        }
    }

    handleProgressUpdate(data) {
        const progressList = document.getElementById('progress-list');
        const timestamp = new Date().toLocaleTimeString();
        
        let icon = 'fas fa-circle-notch fa-spin';
        let message = data.message;
        let url = data.url || '';
        
        // Set appropriate icon based on step
        switch (data.step) {
            case 'intent':
                icon = 'fas fa-brain';
                break;
            case 'search':
                icon = 'fas fa-search';
                break;
            case 'source':
                icon = 'fas fa-globe';
                break;
            case 'pdf':
                icon = 'fas fa-file-pdf';
                break;
            case 'analysis':
                icon = 'fas fa-cogs';
                break;
            case 'complete':
                icon = 'fas fa-check';
                break;
            case 'error':
                icon = 'fas fa-exclamation-triangle';
                break;
        }
        
        const progressItem = document.createElement('div');
        progressItem.className = 'progress-item';
        
        progressItem.innerHTML = `
            <div class="progress-icon">
                <i class="${icon}"></i>
            </div>
            <div class="progress-content">
                <div class="progress-message">${message}</div>
                ${url ? `<a href="${url}" target="_blank" class="progress-url">${url}</a>` : ''}
            </div>
        `;
        
        progressList.appendChild(progressItem);
        
        // Auto-scroll to bottom
        progressList.scrollTop = progressList.scrollHeight;
        
        // Update loading title
        if (data.step !== 'complete' && data.step !== 'error') {
            document.getElementById('loading-title').textContent = message;
        }
    }

    showLoading() {
        document.querySelector('.search-container').style.display = 'none';
        document.getElementById('results').style.display = 'none';
        document.getElementById('error').style.display = 'none';
        document.getElementById('loading').style.display = 'block';
        document.getElementById('research-btn').disabled = true;
    }

    showResults(result, researchInfo) {
        // Clear loading
        document.getElementById('loading').style.display = 'none';
        document.getElementById('research-btn').disabled = false;

        // Show results
        document.getElementById('results').style.display = 'block';

        // Update header
        document.getElementById('results-title').textContent = `Results for "${result.query || this.currentQuery}"`;
        document.getElementById('research-type').textContent = this.formatResearchType(result.research_type);
        
        if (researchInfo.start_time && researchInfo.end_time) {
            const duration = new Date(researchInfo.end_time) - new Date(researchInfo.start_time);
            document.getElementById('research-time').textContent = `${Math.round(duration / 1000)}s`;
        }

        document.getElementById('entity-count').textContent = `${result.entities?.length || 0} results`;

        // Render quick summary
        this.renderQuickSummary(result);

        // Render entities
        this.renderEntities(result.entities, result.research_type);

        // Render analysis
        document.getElementById('analysis-content').textContent = result.analysis || 'No detailed analysis available';
    }

    renderQuickSummary(result) {
        const container = document.getElementById('quick-insights');
        
        if (!result.entities || result.entities.length === 0) {
            container.innerHTML = '<p>No key insights available</p>';
            return;
        }

        const topEntities = result.entities.slice(0, 3);
        const insights = topEntities.map(entity => `• ${entity.name}`).join('<br>');
        
        container.innerHTML = `
            <p><strong>Top Results:</strong></p>
            <div style="margin-top: 8px; color: var(--text-secondary);">${insights}</div>
        `;
    }

    renderEntities(entities, researchType) {
        const container = document.getElementById('entities');
        
        if (!entities || entities.length === 0) {
            container.innerHTML = '<div class="empty-state">No entities found</div>';
            return;
        }

        const html = entities.map(entity => {
            const typeColor = this.getTypeColor(entity.type);
            
            return `
                <div class="entity-card">
                    <div class="entity-header">
                        <div>
                            <div class="entity-name">${entity.name}</div>
                            ${entity.website ? `<a href="${entity.website}" target="_blank" class="entity-website">${this.formatUrl(entity.website)}</a>` : ''}
                        </div>
                        <span class="entity-type" style="background-color: ${typeColor}; color: white;">${entity.type}</span>
                    </div>
                    
                    ${entity.description ? `<div class="entity-description">${entity.description}</div>` : ''}
                    
                    <div class="entity-details">
                        ${this.renderEntityDetails(entity.details, researchType)}
                    </div>
                </div>
            `;
        }).join('');

        container.innerHTML = html;
    }

    renderEntityDetails(details, researchType) {
        if (!details) return '';

        return Object.entries(details).map(([key, value]) => {
            if (!value || value === 'Unknown' || (Array.isArray(value) && value.length === 0)) {
                return '';
            }

            const label = this.formatDetailLabel(key);
            const formattedValue = this.formatDetailValue(value);

            return `
                <div class="detail-item">
                    <div class="detail-label">${label}</div>
                    <div class="detail-value">${formattedValue}</div>
                </div>
            `;
        }).filter(item => item).join('');
    }

    showError(message) {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('results').style.display = 'none';
        document.getElementById('research-btn').disabled = false;

        document.getElementById('error-message').textContent = message;
        document.getElementById('error').style.display = 'block';
    }

    addToHistory(query) {
        // Add to recent searches (simplified)
        const historyList = document.getElementById('history-list');
        const newItem = document.createElement('div');
        newItem.className = 'history-item';
        newItem.innerHTML = `
            <i class="fas fa-clock"></i>
            <span>${query.substring(0, 30)}${query.length > 30 ? '...' : ''}</span>
        `;
        
        newItem.addEventListener('click', () => {
            document.getElementById('query').value = query;
            this.currentQuery = query;
            this.autoResize(document.getElementById('query'));
        });
        
        historyList.insertBefore(newItem, historyList.firstChild);
        
        // Keep only last 5 items
        while (historyList.children.length > 5) {
            historyList.removeChild(historyList.lastChild);
        }
    }

    exportResults() {
        // Simple export functionality
        const results = document.getElementById('results');
        if (results.style.display !== 'none') {
            const content = results.innerText;
            const blob = new Blob([content], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `research-results-${new Date().toISOString().split('T')[0]}.txt`;
            a.click();
            URL.revokeObjectURL(url);
        }
    }

    shareResults() {
        // Simple share functionality
        if (navigator.share) {
            navigator.share({
                title: 'Research Results',
                text: 'Check out these research results from Multi Agent Researcher',
                url: window.location.href
            });
        } else {
            // Fallback: copy to clipboard
            navigator.clipboard.writeText(window.location.href).then(() => {
                alert('Link copied to clipboard!');
            });
        }
    }

    initDarkMode() {
        // Check for saved theme preference or default to light mode
        const savedTheme = localStorage.getItem('theme') || 'light';
        this.setTheme(savedTheme);
    }

    toggleDarkMode() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }

    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        
        // Update dark mode button icon
        const darkModeBtn = document.getElementById('dark-mode-btn');
        const icon = darkModeBtn.querySelector('i');
        
        if (theme === 'dark') {
            icon.className = 'fas fa-sun';
            darkModeBtn.title = 'Switch to Light Mode';
        } else {
            icon.className = 'fas fa-moon';
            darkModeBtn.title = 'Switch to Dark Mode';
        }
    }

    startNewSearch() {
        // Clear current results and return to search interface
        document.getElementById('results').style.display = 'none';
        document.getElementById('error').style.display = 'none';
        document.getElementById('loading').style.display = 'none';
        document.querySelector('.search-container').style.display = 'block';
        
        // Clear the search input
        const textarea = document.getElementById('query');
        textarea.value = '';
        this.currentQuery = '';
        this.autoResize(textarea);
        
        // Reset selected PDFs
        this.selectedPdfs = [];
        
        // Focus on search input
        textarea.focus();
        
        // Reset research mode to auto if needed
        const autoMode = document.querySelector('input[name="research-mode"][value="auto"]');
        if (autoMode) {
            autoMode.checked = true;
            this.handleModeChange('auto');
        }
    }

    // Utility functions
    formatResearchType(type) {
        const types = {
            'developer_tools': 'Developer Tools',
            'product_research': 'Product Research',
            'educational_research': 'Educational Research',
            'financial_research': 'Financial Research',
            'technical_research': 'Technical Research',
            'industry_research': 'Industry Research',
            'market_research': 'Market Research',
            'general_research': 'General Research'
        };
        return types[type] || type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    getTypeColor(type) {
        const colors = {
            'company': '#2563eb',
            'product': '#10b981',
            'university': '#06b6d4',
            'financial': '#f59e0b',
            'technical': '#8b5cf6',
            'industry': '#f97316'
        };
        return colors[type] || '#64748b';
    }

    formatDetailLabel(key) {
        const labels = {
            'pricing': 'Pricing',
            'open_source': 'Open Source',
            'tech_stack': 'Tech Stack',
            'api_available': 'API',
            'languages': 'Languages',
            'integrations': 'Integrations'
        };
        return labels[key] || key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    formatDetailValue(value) {
        if (Array.isArray(value)) {
            if (value.length === 0) return 'None';
            return `<div class="detail-list">${value.map(item => `<span class="detail-tag">${item}</span>`).join('')}</div>`;
        }
        
        if (typeof value === 'boolean') {
            return value ? '✅ Yes' : '❌ No';
        }
        
        return value;
    }

    formatUrl(url) {
        try {
            return new URL(url).hostname.replace('www.', '');
        } catch {
            return url;
        }
    }
}

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    new ModernResearchAgent();
});