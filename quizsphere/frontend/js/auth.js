const API_URL = 'https://quizsphere-bay.vercel.app';
// const API_URL = 'http://localhost:8000';

const auth = {
    getToken: () => localStorage.getItem('access_token'),
    setToken: (token) => localStorage.setItem('access_token', token),
    removeToken: () => localStorage.removeItem('access_token'),
    isLoggedIn: () => !!localStorage.getItem('access_token'),
    getUser: async () => {
        if (!auth.isLoggedIn()) return null;
        try {
            const response = await fetch(`${API_URL}/auth/me`, {
                headers: { 'Authorization': `Bearer ${auth.getToken()}` }
            });
            if (response.ok) return await response.json();

            if (response.status === 401) {
                console.warn('Session expired, clearing token');
                auth.removeToken();
                const isAuthPage = window.location.pathname.includes('login.html') ||
                    window.location.pathname.includes('register.html');
                if (!isAuthPage) {
                    window.location.href = 'login.html';
                }
            }
        } catch (err) {
            console.error('Auth check failed:', err);
        }
        return null;
    },
    renderAvatar: (element, user) => {
        if (!element || !user) return;
        if (user.avatar_url && user.avatar_url.startsWith('http')) {
            element.innerHTML = `<img src="${user.avatar_url}" alt="${user.full_name}" class="avatar-img-round">`;
            element.classList.add('has-image');
        } else {
            element.innerText = user.full_name.charAt(0).toUpperCase();
            element.classList.remove('has-image');
        }
    }
};

const protectedRoutes = ['dashboard.html', 'profile.html', 'create-quiz.html', 'take-quiz.html', 'result.html'];
const currentPage = window.location.pathname.split('/').pop();

if (protectedRoutes.includes(currentPage) && !auth.isLoggedIn()) {
    window.location.href = 'login.html?redirect=' + currentPage;
}

const initAuth = async () => {
    console.log('QuizSphere UI Initializing...');

    try {
        if (typeof AOS !== 'undefined') {
            AOS.init({
                duration: 800,
                once: true,
                offset: 100
            });
            console.log('AOS Initialized');
        } else {
            console.warn('AOS library not found, content may be hidden');
        }
    } catch (e) {
        console.error('AOS init failed:', e);
    }

    const authLinks = document.getElementById('auth-links');
    const userLinks = document.getElementById('user-links');
    const userNameDisplay = document.getElementById('user-name-nav');
    const userAvatar = document.getElementById('user-avatar');
    const logoutBtn = document.getElementById('logout-btn');
    const themeToggle = document.getElementById('theme-toggle');

    if (auth.isLoggedIn()) {
        const user = await auth.getUser();
        if (user) {
            if (authLinks) authLinks.style.display = 'none';
            if (userLinks) {
                userLinks.style.display = 'flex';
                if (userNameDisplay) userNameDisplay.innerText = user.full_name.split(' ')[0];
                if (userAvatar) {
                    auth.renderAvatar(userAvatar, user);
                }
            }
        }
    } else {
        if (authLinks) authLinks.style.display = 'flex';
        if (userLinks) userLinks.style.display = 'none';
    }

    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            auth.removeToken();
            window.location.href = 'index.html';
        });
    }

    if (themeToggle) {
        const currentTheme = localStorage.getItem('theme') || 'light';
        if (currentTheme === 'dark') {
            document.body.classList.add('dark-mode');
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        }

        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
            const theme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
            localStorage.setItem('theme', theme);
            themeToggle.innerHTML = theme === 'dark' ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
        });
    }

    window.showAuthModal = (message = "Please login or create an account to continue.") => {
        const modalHtml = `
            <div id="auth-modal" class="modal-overlay fade-in">
                <div class="modal-card glass card-modern">
                    <div class="modal-header">
                        <i class="fas fa-lock fa-3x gradient-text mb-3"></i>
                        <h2>Authentication Required</h2>
                        <p class="text-muted">${message}</p>
                    </div>
                    <div class="modal-body mt-4">
                        <a href="login.html" class="btn btn-primary w-full mb-3">Login</a>
                        <a href="register.html" class="btn btn-secondary w-full">Create Account</a>
                    </div>
                    <button class="modal-close" onclick="document.getElementById('auth-modal').remove()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHtml);
    };

    window.showToast = (title, message, type = 'success') => {
        const toastHtml = `
            <div class="toast-notification ${type} fade-in">
                <div class="toast-icon">
                    <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-triangle'}"></i>
                </div>
                <div class="toast-content">
                    <strong>${title}</strong>
                    <p>${message}</p>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', toastHtml);
        const toast = document.querySelector('.toast-notification:last-child');
        setTimeout(() => {
            if (toast) {
                toast.classList.add('fade-out');
                setTimeout(() => toast.remove(), 500);
            }
        }, 3000);
    };

    document.querySelectorAll('[data-auth-required]').forEach(el => {
        el.addEventListener('click', (e) => {
            if (!auth.isLoggedIn()) {
                e.preventDefault();
                showAuthModal();
            }
        });
    });

    const counters = document.querySelectorAll('.counter');
    const speed = 200;

    const startCounters = () => {
        counters.forEach(counter => {
            const updateCount = () => {
                const target = +counter.getAttribute('data-target');
                const count = +counter.innerText.replace(/,/g, '');
                const inc = target / speed;

                if (count < target) {
                    counter.innerText = Math.ceil(count + inc);
                    setTimeout(updateCount, 1);
                } else {
                    counter.innerText = target.toLocaleString() + '+';
                }
            };
            updateCount();
        });
    };

    const statsSection = document.querySelector('.stats-section');
    if (statsSection) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    startCounters();
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        observer.observe(statsSection);
    }

    const navbar = document.getElementById('main-nav');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        console.log('Login form found, attaching listener...');
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const emailInput = document.getElementById('email');
            const passwordInput = document.getElementById('password');
            const email = emailInput.value;
            const password = passwordInput.value;
            const errorMsg = document.getElementById('error-message');
            const submitBtn = loginForm.querySelector('button[type="submit"]');

            if (errorMsg) errorMsg.style.display = 'none';
            submitBtn.disabled = true;
            const originalBtnText = submitBtn.innerText;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Authenticating...';

            const params = new URLSearchParams();
            params.append('username', email);
            params.append('password', password);

            try {
                console.log('Attempting login for:', email);
                const response = await fetch(`${API_URL}/auth/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: params
                });

                if (response.ok) {
                    const data = await response.json();
                    console.log('Login successful');
                    auth.setToken(data.access_token);
                    showToast('Success', 'Login Successful!', 'success');

                    const redirect = new URLSearchParams(window.location.search).get('redirect') || 'dashboard.html';
                    setTimeout(() => window.location.href = redirect, 1000);
                } else {
                    const errorData = await response.json().catch(() => ({}));
                    console.error('Login failed:', response.status, errorData);
                    if (errorMsg) {
                        errorMsg.style.display = 'flex';
                        const errorSpan = errorMsg.querySelector('span');
                        if (errorSpan && errorData.detail) {
                            errorSpan.innerText = errorData.detail;
                        }
                    }
                    submitBtn.disabled = false;
                    submitBtn.innerText = originalBtnText;
                }
            } catch (err) {
                console.error('Login request error:', err);
                showToast('Error', 'Unable to connect to server. Please ensure backend is running.', 'danger');
                submitBtn.disabled = false;
                submitBtn.innerText = originalBtnText;
            }
        });
    }

    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const fullname = document.getElementById('fullname').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm-password').value;
            const submitBtn = registerForm.querySelector('button[type="submit"]');

            if (password !== confirmPassword) {
                showToast('Error', 'Passwords do not match', 'danger');
                return;
            }

            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating Account...';

            try {
                const response = await fetch(`${API_URL}/auth/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ full_name: fullname, email, password })
                });

                if (response.ok) {
                    showToast('Success', 'Account created!', 'success');
                    setTimeout(() => window.location.href = 'login.html', 1500);
                } else {
                    const data = await response.json();
                    showToast('Error', data.detail || 'Registration failed', 'danger');
                    submitBtn.disabled = false;
                }
            } catch (err) {
                console.error(err);
                submitBtn.disabled = false;
            }
        });
    }

    const togglePassword = document.getElementById('toggle-password');
    const passwordInput = document.getElementById('password');
    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', () => {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            togglePassword.classList.toggle('fa-eye');
            togglePassword.classList.toggle('fa-eye-slash');
        });
    }

    const strengthBar = document.getElementById('strength-bar');
    if (passwordInput && strengthBar) {
        passwordInput.addEventListener('input', () => {
            const val = passwordInput.value;
            let strength = 0;
            if (val.length >= 8) strength++;
            if (/[A-Z]/.test(val)) strength++;
            if (/[0-9]/.test(val)) strength++;
            if (/[^A-Za-z0-9]/.test(val)) strength++;

            strengthBar.className = 'strength-bar';
            if (strength === 1) strengthBar.classList.add('strength-weak');
            if (strength >= 2 && strength <= 3) strengthBar.classList.add('strength-medium');
            if (strength === 4) strengthBar.classList.add('strength-strong');
        });
    }
};

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAuth);
} else {
    initAuth();
}

// Mobile Menu Toggle
document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById("mobile-menu-btn");
    const navLinks = document.querySelector(".nav-links");
    if (toggleBtn && navLinks) {
        toggleBtn.addEventListener("click", () => {
            navLinks.classList.toggle("active");
        });
    }
});

