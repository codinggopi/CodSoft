const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const API_BASE_URL = isLocal ? "http://localhost:8000" : "https://careerconnect-navy.vercel.app";

// Intercept fetch to log request URL
const originalFetch = window.fetch;
window.fetch = async function () {
    console.log("Request URL:", arguments[0]);
    return originalFetch.apply(this, arguments);
};
