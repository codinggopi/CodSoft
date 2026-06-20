const API_URL = "https://careerconnect-navy.vercel.app";

document.addEventListener('DOMContentLoaded', () => {
    // Login Form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            const formData = new URLSearchParams();
            formData.append('username', email);
            formData.append('password', password);

            try {
                const response = await fetch(`${API_URL}/users/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: formData
                });

                if (response.ok) {
                    const data = await response.json();
                    localStorage.setItem('token', data.access_token);

                    // Fetch profile to redirect based on role
                    const profileRes = await fetch(`${API_URL}/users/profile`, {
                        headers: { 'Authorization': `Bearer ${data.access_token}` }
                    });

                    if (profileRes.ok) {
                        const profile = await profileRes.json();
                        localStorage.setItem('user', JSON.stringify(profile));

                        if (profile.role === 'admin') window.location.href = 'admin-dashboard.html';
                        else if (profile.role === 'employer') window.location.href = 'employer-dashboard.html';
                        else window.location.href = 'candidate-dashboard.html';
                    }
                } else {
                    const err = await response.json();
                    alert(err.detail || "Login failed");
                }
            } catch (error) {
                console.error('Error:', error);
                alert("An error occurred during login.");
            }
        });
    }

    // Register Form
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const phone = document.getElementById('phone').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            const role = document.querySelector('input[name="role"]:checked').value;
            const security_question = document.getElementById('securityQuestion').value;
            const security_answer = document.getElementById('securityAnswer').value;

            if (password !== confirmPassword) {
                alert("Passwords do not match!");
                return;
            }

            let payload = {
                name,
                email,
                phone,
                role,
                password,
                security_question,
                security_answer,
                company_name: null,
                company_email: null,
                industry: null,
                website: null
            };

            if (role === 'employer') {
                payload.company_name = document.getElementById('companyName').value;
                payload.company_email = document.getElementById('companyEmail').value;
                payload.industry = document.getElementById('industry').value;
                payload.website = document.getElementById('website').value || null;

                if (!payload.company_name || !payload.company_email || !payload.industry) {
                    const validationError = "Validation Error: Company name, company email, and industry are required for employers.";
                    console.error(validationError);
                    alert(validationError);
                    return;
                }
            }

            console.log("Request Payload:", JSON.stringify(payload, null, 2));

            try {
                const response = await fetch(`${API_URL}/users/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const responseBody = await response.json();
                console.log("Response Status:", response.status);
                console.log("Response Body:", JSON.stringify(responseBody, null, 2));

                if (response.ok) {
                    alert("Registration successful! Please login.");
                    window.location.href = 'login.html';
                } else {
                    let errorMessage = "Registration failed. Please check your input.";
                    if (responseBody.detail) {
                        if (Array.isArray(responseBody.detail)) {
                            errorMessage = responseBody.detail.map(err => `${err.loc[1]}: ${err.msg}`).join('\n');
                        } else {
                            errorMessage = responseBody.detail;
                        }
                    }
                    console.error("Validation Errors:", errorMessage);
                    alert(errorMessage);
                }
            } catch (error) {
                console.error('Error during registration:', error);
                alert("An error occurred during registration. Please try again later.");
            }
        });
    }
});


// Utility to check auth and redirect
function checkAuth(allowedRoles = []) {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
        return null;
    }

    const userStr = localStorage.getItem('user');
    if (userStr) {
        const user = JSON.parse(userStr);
        if (allowedRoles.length > 0 && !allowedRoles.includes(user.role)) {
            alert("Unauthorized access");
            window.location.href = 'index.html';
            return null;
        }
        return user;
    }
    return null;
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}
