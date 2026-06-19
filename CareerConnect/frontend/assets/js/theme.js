document.addEventListener('DOMContentLoaded', () => {
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');

    // Check for saved theme preference or system preference
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && systemPrefersDark)) {
        document.documentElement.setAttribute('data-theme', 'dark');
        if (themeIcon) {
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
        }
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            if (currentTheme === 'dark') {
                document.documentElement.removeAttribute('data-theme');
                localStorage.setItem('theme', 'light');
                themeIcon.classList.remove('fa-sun');
                themeIcon.classList.add('fa-moon');
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                themeIcon.classList.remove('fa-moon');
                themeIcon.classList.add('fa-sun');
            }
        });
    }

    // Password Toggle Logic
    const passwordToggles = document.querySelectorAll('.password-toggle');
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function () {
            const input = this.previousElementSibling;
            if (input.type === 'password') {
                input.type = 'text';
                this.classList.remove('fa-eye');
                this.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                this.classList.remove('fa-eye-slash');
                this.classList.add('fa-eye');
            }
        });
    });

    // Dropdown Toggle Logic
    window.toggleDropdown = function(id) {
        const dropdown = document.getElementById(id);
        if (dropdown) {
            dropdown.classList.toggle('active');
        }
    }

    // Close dropdowns when clicking outside
    document.addEventListener('click', (event) => {
        if (!event.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown').forEach(d => d.classList.remove('active'));
        }
    });

    setupGlobalNavbar();
});

function setupGlobalNavbar() {
    const navLinks = document.querySelector('.nav-links');
    if (!navLinks) return;

    const token = localStorage.getItem('token');
    const userStr = localStorage.getItem('user');
    
    const themeToggle = document.getElementById('theme-toggle');
    const themeIconHtml = themeToggle ? themeToggle.outerHTML : `<button id="theme-toggle" class="theme-toggle" aria-label="Toggle Theme"><i id="theme-icon" class="fas fa-moon"></i></button>`;

    let linksHtml = '';
    
    if (token && userStr) {
        const user = JSON.parse(userStr);
        let dashboardUrl = 'candidate-dashboard.html';
        
        if (user.role === 'admin') dashboardUrl = 'admin-dashboard.html';
        else if (user.role === 'employer') dashboardUrl = 'employer-dashboard.html';

        const profileData = JSON.parse(localStorage.getItem(`profile_${user.id}`) || '{}');
        const defaultPic = 'https://ui-avatars.com/api/?name=' + encodeURIComponent(user.name) + '&background=166534&color=fff';
        const profilePic = profileData.image || defaultPic;

        if (user.role === 'employer') {
            linksHtml += `
                <a href="index.html">Home</a>
                <a href="post-job.html">Post Job</a>
                <a href="manage-jobs.html">Manage Jobs</a>
                <a href="applicants.html">Applicants</a>
                <a href="company-profile.html">Company Profile</a>
            `;
        } else if (user.role === 'candidate') {
            linksHtml += `
                <a href="index.html">Home</a>
                <a href="jobs.html">Find Jobs</a>
                <a href="candidate-dashboard.html">My Applications</a>
                <a href="resume.html">Resume</a>
                <a href="profile.html">Profile</a>
            `;
        } else if (user.role === 'admin') {
             linksHtml += `
                <a href="index.html">Home</a>
                <a href="admin-dashboard.html">Dashboard</a>
             `;
        }
        
        linksHtml += `
            <div class="dropdown" id="profileDropdown">
                <div class="profile-trigger" onclick="toggleDropdown('profileDropdown')">
                    <img src="${profilePic}" alt="Profile">
                    <span style="font-weight: 500;">${user.name}</span>
                    <i class="fas fa-chevron-down" style="font-size: 0.8rem; color: var(--text-muted);"></i>
                </div>
                <div class="dropdown-content">
                    <a href="${dashboardUrl}"><i class="fas fa-columns mr-2"></i> Dashboard</a>
                    ${user.role === 'employer' ? `<a href="employer-profile.html"><i class="fas fa-user mr-2"></i> My Profile</a>` : ''}
                    ${user.role === 'candidate' ? `<a href="profile.html"><i class="fas fa-user mr-2"></i> My Profile</a>` : ''}
                    ${user.role === 'employer' ? `<a href="company-profile.html"><i class="fas fa-building mr-2"></i> Company Profile</a>` : ''}
                    ${user.role !== 'admin' ? `<a href="settings.html"><i class="fas fa-cog mr-2"></i> Settings</a>` : ''}
                    <a href="#" onclick="logoutUser(event)"><i class="fas fa-sign-out-alt mr-2"></i> Logout</a>
                </div>
            </div>
        `;
    } else {
        linksHtml += `
            <a href="index.html">Home</a>
            <a href="about.html">About</a>
            <a href="contact.html">Contact</a>
            <a href="login.html" class="btn btn-outline" style="padding: 0.5rem 1rem;">Login</a>
            <a href="register.html" class="btn btn-primary" style="padding: 0.5rem 1rem;">Register</a>
        `;
    }

    navLinks.innerHTML = linksHtml + themeIconHtml;

    const newThemeToggle = document.getElementById('theme-toggle');
    const newThemeIcon = document.getElementById('theme-icon');
    if (newThemeToggle) {
        newThemeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            if (currentTheme === 'dark') {
                document.documentElement.removeAttribute('data-theme');
                localStorage.setItem('theme', 'light');
                newThemeIcon.classList.remove('fa-sun');
                newThemeIcon.classList.add('fa-moon');
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                newThemeIcon.classList.remove('fa-moon');
                newThemeIcon.classList.add('fa-sun');
            }
        });
        
        const currentTheme = document.documentElement.getAttribute('data-theme');
        if(currentTheme === 'dark') {
            newThemeIcon.classList.remove('fa-moon');
            newThemeIcon.classList.add('fa-sun');
        }
    }
}

function enforceRouteProtection() {
    const path = window.location.pathname.toLowerCase();
    const token = localStorage.getItem('token');
    const userStr = localStorage.getItem('user');
    const user = userStr ? JSON.parse(userStr) : null;
    const role = user ? user.role : 'guest';

    const candidateRoutes = ['candidate-dashboard.html', 'resume.html', 'profile.html', 'job-details.html', 'jobs.html'];
    const employerRoutes = ['employer-dashboard.html', 'employer-profile.html', 'company-profile.html', 'edit-company-profile.html', 'post-job.html', 'manage-jobs.html', 'applicants.html', 'employer-analytics.html'];
    const adminRoutes = ['admin-dashboard.html'];

    const filename = path.split('/').pop().split('?')[0].split('#')[0];

    if (candidateRoutes.includes(filename)) {
        if (role !== 'candidate' && role !== 'admin') {
            if (role === 'guest') window.location.href = 'login.html';
            else window.location.href = 'employer-dashboard.html';
        }
    }

    if (employerRoutes.includes(filename)) {
        if (role !== 'employer' && role !== 'admin') {
            if (role === 'guest') window.location.href = 'login.html';
            else window.location.href = 'candidate-dashboard.html';
        }
    }
    
    if (adminRoutes.some(r => path.includes(r))) {
        if (role !== 'admin') {
            if (role === 'guest') window.location.href = 'login.html';
            else window.location.href = 'index.html';
        }
    }
}
enforceRouteProtection();

function logoutUser(e) {
    e.preventDefault();
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}
