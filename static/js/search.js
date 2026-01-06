/**
 * Jassas Search - Client-side search handling
 */

const API_URL = '/api/v1/search';

// DOM Elements
const searchForm = document.getElementById('search-form');
const searchInput = document.getElementById('search-input');
const resultsStats = document.getElementById('results-stats');
const resultsContainer = document.getElementById('results-container');

/**
 * Get query parameter from URL
 */
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

/**
 * Update URL with query parameter (without reload)
 */
function updateURL(query) {
    const url = new URL(window.location);
    url.searchParams.set('q', query);
    history.pushState({}, '', url);
    document.title = `${query} - جساس`;
}

/**
 * Render search results
 */
function renderResults(data) {
    // Update stats
    resultsStats.textContent = `${data.count} نتيجة (${data.execution_time_ms} مللي ثانية)`;

    // Clear container
    resultsContainer.innerHTML = '';

    if (data.results.length === 0) {
        resultsContainer.innerHTML = `
            <div class="no-results">
                <p>لا توجد نتائج لـ "${data.query}"</p>
            </div>
        `;
        return;
    }

    // Render each result
    data.results.forEach(result => {
        const domain = new URL(result.url).hostname.replace('www.', '');
        const card = document.createElement('a');
        card.className = 'result-card';
        card.href = result.url;
        card.target = '_blank';
        card.innerHTML = `
            <span class="result-domain">${escapeHtml(domain)}</span>
            <h3 class="result-title">${escapeHtml(result.title)}</h3>
            <p class="result-snippet">${escapeHtml(result.snippet)}</p>
        `;
        resultsContainer.appendChild(card);
    });
}

/**
 * Show loading state
 */
function showLoading() {
    resultsStats.textContent = 'جاري البحث...';
    resultsContainer.innerHTML = '<div class="loading"></div>';
}

/**
 * Show error message
 */
function showError(message) {
    resultsStats.textContent = '';
    resultsContainer.innerHTML = `
        <div class="no-results">
            <p>${escapeHtml(message)}</p>
        </div>
    `;
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Execute search
 */
async function executeSearch(query) {
    if (!query || query.length < 2) {
        showError('يجب أن يكون البحث على الأقل حرفين');
        return;
    }

    showLoading();
    updateURL(query);

    try {
        const response = await fetch(`${API_URL}?q=${encodeURIComponent(query)}&limit=10`);

        if (!response.ok) {
            throw new Error('فشل في الاتصال بالخادم');
        }

        const data = await response.json();
        renderResults(data);
    } catch (error) {
        console.error('Search error:', error);
        showError('حدث خطأ أثناء البحث. حاول مرة أخرى.');
    }
}

/**
 * Handle form submission
 */
searchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const query = searchInput.value.trim();
    executeSearch(query);
});

/**
 * Handle browser back/forward
 */
window.addEventListener('popstate', () => {
    const query = getQueryParam('q');
    if (query) {
        searchInput.value = query;
        executeSearch(query);
    }
});

/**
 * Initialize on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    const query = getQueryParam('q');
    if (query) {
        searchInput.value = query;
        executeSearch(query);
    }
});
