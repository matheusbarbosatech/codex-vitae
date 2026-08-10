// Main JavaScript file for Codex Vitae SaaS

document.addEventListener('DOMContentLoaded', () => {
    console.log('Codex Vitae SaaS loaded successfully.');
});

// Helper for calling API endpoints with authorization header fallback
async function fetchApi(url, options = {}) {
    options.headers = options.headers || {};
    options.headers['Content-Type'] = 'application/json';

    // Get token from localStorage if present
    const token = localStorage.getItem('token');
    if (token) {
        options.headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(url, options);
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || 'Ocorreu um erro na requisição.');
    }
    return data;
}
