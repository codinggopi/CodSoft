document.addEventListener('DOMContentLoaded', async () => {
    if (!auth.isLoggedIn()) return;

    const profileLoading = document.getElementById('profile-loading');
    const profileContent = document.getElementById('profile-content');
    const dashLoading = document.getElementById('dashboard-loading');
    const dashContent = document.getElementById('dashboard-content');

    if (profileLoading) profileLoading.style.display = 'block';
    if (profileContent) profileContent.style.display = 'none';
    if (dashLoading) dashLoading.style.display = 'block';
    if (dashContent) dashContent.style.display = 'none';

    const profileFullname = document.getElementById('profile-fullname');
    const userNameNav = document.getElementById('user-name');
    if (profileFullname || userNameNav) {
        try {
            const response = await fetch(`${API_URL}/auth/me`, {
                headers: { 'Authorization': `Bearer ${auth.getToken()}` }
            });
            const user = await response.json();
            
            if (profileFullname) {
                profileFullname.innerText = user.full_name;
                document.getElementById('profile-email').innerText = user.email;
                if (user.bio) {
                    document.getElementById('profile-bio').innerText = user.bio;
                }
                document.getElementById('profile-joined').innerText = new Date(user.created_at).toLocaleDateString('en-US', {
                    year: 'numeric', month: 'long', day: 'numeric'
                });

                const largeAvatar = document.getElementById('profile-avatar-large');
                if (largeAvatar) {
                    auth.renderAvatar(largeAvatar, user);
                }
            }
            
            if (userNameNav) {
                userNameNav.innerText = user.full_name.split(' ')[0];
            }

            if (profileLoading) profileLoading.style.display = 'none';
            if (profileContent) profileContent.style.display = 'block';
            if (dashLoading) dashLoading.style.display = 'none';
            if (dashContent) dashContent.style.display = 'block';
            if (typeof AOS !== 'undefined') AOS.refresh();

        } catch (err) {
            console.error(err);
        }
    }

    if (document.getElementById('quizzes-created')) {
        try {
            const response = await fetch(`${API_URL}/users/stats`, {
                headers: { 'Authorization': `Bearer ${auth.getToken()}` }
            });
            const stats = await response.json();
            
            animateCounter('quizzes-created', stats.quizzes_created);
            animateCounter('quizzes-attempted', stats.quizzes_attempted);
            
            document.getElementById('avg-score').innerText = `${stats.average_score}%`;
            document.getElementById('highest-score').innerText = `${stats.highest_score}%`;
        } catch (err) {
            console.error(err);
        }
    }

    const myQuizzesList = document.getElementById('my-quizzes-list');
    if (myQuizzesList) {
        try {
            const response = await fetch(`${API_URL}/users/my-quizzes`, {
                headers: { 'Authorization': `Bearer ${auth.getToken()}` }
            });
            const quizzes = await response.json();
            
            if (quizzes.length > 0) {
                myQuizzesList.innerHTML = '';
                quizzes.forEach(quiz => {
                    const card = document.createElement('div');
                    card.className = 'quiz-card glass p-4 fade-in';
                    card.innerHTML = `
                        <h3>${quiz.title}</h3>
                        <div class="meta-tags mt-2 mb-3">
                            <span class="badge">${quiz.category}</span>
                            <span class="badge">${quiz.difficulty}</span>
                        </div>
                        <div class="text-muted small mb-3">
                            <i class="fas fa-question-circle"></i> ${quiz.question_count} Questions
                        </div>
                        <div class="card-actions">
                            <button class="btn btn-secondary btn-sm flex-1" onclick="window.location.href='create-quiz.html?edit=${quiz.id}'">
                                <i class="fas fa-edit"></i> Edit
                            </button>
                            <button class="btn btn-ghost text-danger btn-sm" onclick="deleteQuiz(${quiz.id})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    `;
                    myQuizzesList.appendChild(card);
                });
            }
        } catch (err) {
            console.error(err);
        }
    }

    const historyBody = document.getElementById('attempt-history-body');
    if (historyBody) {
        try {
            const response = await fetch(`${API_URL}/attempts/history`, {
                headers: { 'Authorization': `Bearer ${auth.getToken()}` }
            });
            const history = await response.json();
            
            if (history.length > 0) {
                historyBody.innerHTML = '';
                history.forEach(attempt => {
                    const statusClass = attempt.percentage >= 80 ? 'text-success' : (attempt.percentage >= 50 ? 'text-primary' : 'text-warning');
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td><span class="font-bold">${attempt.quiz_title}</span></td>
                        <td>${new Date(attempt.attempted_at).toLocaleDateString()}</td>
                        <td>${attempt.score} Correct</td>
                        <td style="display: flex; gap: 10px; align-items: center;">
                            <span class="badge ${statusClass}">${attempt.percentage.toFixed(1)}%</span>
                            <button class="btn btn-ghost btn-sm" onclick='viewHistoricalReport(${JSON.stringify(attempt).replace(/'/g, "&#39;")})' title="View & Download Report">
                                <i class="fas fa-download"></i>
                            </button>
                        </td>
                    `;
                    historyBody.appendChild(row);
                });
            } else {
                historyBody.innerHTML = '<tr><td colspan="4" class="text-center p-4 text-muted">No attempts yet. Go take a quiz!</td></tr>';
            }
        } catch (err) {
            console.error(err);
        }
    }
});

window.viewHistoricalReport = function(attempt) {
    localStorage.setItem('last_result', JSON.stringify({
        score: attempt.score,
        percentage: attempt.percentage,
        quizTitle: attempt.quiz_title,
        timeTaken: undefined
    }));
    window.location.href = 'result.html';
};

function animateCounter(id, target) {
    const obj = document.getElementById(id);
    let count = 0;
    const speed = 20;
    const increment = target / speed;
    
    const update = () => {
        if (count < target) {
            count += Math.max(increment, 1);
            obj.innerText = Math.floor(count);
            setTimeout(update, 50);
        } else {
            obj.innerText = target;
        }
    };
    update();
}

async function deleteQuiz(id) {
    if (confirm('Are you sure you want to delete this quiz?')) {
        try {
            const response = await fetch(`${API_URL}/quizzes/${id}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${auth.getToken()}` }
            });
            if (response.ok) {
                location.reload();
            }
        } catch (err) {
            console.error(err);
        }
    }
}
