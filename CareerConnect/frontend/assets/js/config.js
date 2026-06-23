const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const API_BASE_URL = isLocal ? "http://localhost:8000" : "https://careerconnect-navy.vercel.app";
