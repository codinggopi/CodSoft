// Quiz Logic for QuizSphere SaaS
document.addEventListener('DOMContentLoaded', () => {
    // 1. MULTI-STEP FORM LOGIC
    const formSteps = document.querySelectorAll('.form-step');
    const nextBtns = document.querySelectorAll('.next-step');
    const prevBtns = document.querySelectorAll('.prev-step');
    const stepperItems = document.querySelectorAll('.stepper-item');

    nextBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const nextStepId = btn.getAttribute('data-next');
            if (validateStep(nextStepId - 1)) {
                goToStep(nextStepId);
            }
        });
    });

    prevBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const prevStepId = btn.getAttribute('data-prev');
            goToStep(prevStepId);
        });
    });

    function goToStep(stepNumber) {
        formSteps.forEach(step => step.classList.remove('active'));
        stepperItems.forEach(item => item.classList.remove('active'));
        
        document.getElementById(`step-${stepNumber}`).classList.add('active');
        document.getElementById(`step-${stepNumber}-indicator`).classList.add('active');
        
        // Mark previous steps as completed
        for (let i = 1; i < stepNumber; i++) {
            document.getElementById(`step-${i}-indicator`).classList.add('completed');
        }

        // Update Review Step if moving to step 3
        if (stepNumber == 3) {
            updateReview();
        }
    }

    function validateStep(stepNumber) {
        const currentStep = document.getElementById(`step-${stepNumber}`);
        const inputs = currentStep.querySelectorAll('input[required], select[required]');
        let valid = true;
        
        inputs.forEach(input => {
            if (!input.value) {
                input.classList.add('is-invalid');
                valid = false;
            } else {
                input.classList.remove('is-invalid');
            }
        });

        if (stepNumber == 2) {
            const questions = document.querySelectorAll('.question-builder-card');
            if (questions.length === 0) {
                alert('Please add at least one question');
                valid = false;
            }
        }

        return valid;
    }

    function updateReview() {
        document.getElementById('review-title').innerText = document.getElementById('quiz-title').value;
        document.getElementById('review-category').innerText = document.getElementById('quiz-category').value;
        document.getElementById('review-difficulty').innerText = document.getElementById('quiz-difficulty').value;
        const qCount = document.querySelectorAll('.question-builder-card').length;
        document.getElementById('review-questions').innerText = `${qCount} Questions`;
    }

    // 2. QUESTION BUILDER LOGIC
    const questionsContainer = document.getElementById('questions-container');
    const addQuestionBtn = document.getElementById('add-question-btn');
    let questionCount = 0;

    function addQuestion() {
        questionCount++;
        const div = document.createElement('div');
        div.className = 'question-builder-card glass p-3 mb-3 fade-in';
        div.innerHTML = `
            <div class="card-header mb-3">
                <span class="badge">Question ${questionCount}</span>
                <button type="button" class="btn btn-ghost text-danger remove-q" onclick="this.closest('.question-builder-card').remove()">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
            <div class="form-group mb-3">
                <label>Question Text</label>
                <input type="text" class="form-control q-text" required placeholder="What is the output of... ?">
            </div>
            <div class="options-inputs">
                <div class="opt-group">
                    <label>Option A</label>
                    <input type="text" class="form-control opt-a" required placeholder="Option A">
                </div>
                <div class="opt-group">
                    <label>Option B</label>
                    <input type="text" class="form-control opt-b" required placeholder="Option B">
                </div>
                <div class="opt-group">
                    <label>Option C</label>
                    <input type="text" class="form-control opt-c" required placeholder="Option C">
                </div>
                <div class="opt-group">
                    <label>Option D</label>
                    <input type="text" class="form-control opt-d" required placeholder="Option D">
                </div>
            </div>
            <div class="form-group mt-3">
                <label>Correct Answer</label>
                <select class="form-control q-correct" required>
                    <option value="A">Option A</option>
                    <option value="B">Option B</option>
                    <option value="C">Option C</option>
                    <option value="D">Option D</option>
                </select>
            </div>
        `;
        questionsContainer.appendChild(div);
        div.scrollIntoView({ behavior: 'smooth', block: 'end' });
    }

    if (addQuestionBtn) {
        addQuestionBtn.addEventListener('click', addQuestion);
        if (questionCount === 0) addQuestion();
    }

    // Form Submission
    const createQuizForm = document.getElementById('create-quiz-form');
    if (createQuizForm) {
        createQuizForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const submitBtn = createQuizForm.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Publishing...';

            const quizData = {
                title: document.getElementById('quiz-title').value,
                description: document.getElementById('quiz-desc').value,
                category: document.getElementById('quiz-category').value,
                difficulty: document.getElementById('quiz-difficulty').value,
                timer: parseInt(document.getElementById('quiz-timer').value),
                questions: []
            };

            const cards = document.querySelectorAll('.question-builder-card');
            cards.forEach(card => {
                quizData.questions.push({
                    question_text: card.querySelector('.q-text').value,
                    option_a: card.querySelector('.opt-a').value,
                    option_b: card.querySelector('.opt-b').value,
                    option_c: card.querySelector('.opt-c').value,
                    option_d: card.querySelector('.opt-d').value,
                    correct_answer: card.querySelector('.q-correct').value
                });
            });

            try {
                const response = await fetch(`${API_URL}/quizzes/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${auth.getToken()}`
                    },
                    body: JSON.stringify(quizData)
                });

                if (response.ok) {
                    showToast('Success', 'Quiz published successfully!', 'success');
                    setTimeout(() => window.location.href = 'dashboard.html', 1500);
                } else {
                    showToast('Error', 'Failed to publish quiz', 'danger');
                    submitBtn.disabled = false;
                    submitBtn.innerText = 'Publish Quiz Now';
                }
            } catch (err) {
                console.error(err);
                submitBtn.disabled = false;
            }
        });
    }

    // 3. PREMIUM QUIZ TAKING LOGIC
    const quizTakeId = new URLSearchParams(window.location.search).get('id');
    if (quizTakeId && document.getElementById('question-text')) {
        let currentQuestions = [];
        let currentIndex = 0;
        let userAnswers = {};
        let timeLeft = 0;
        let totalTime = 0;
        let timerInterval;

        async function startQuiz() {
            try {
                // Show loading, hide content
                document.getElementById('quiz-loading').style.display = 'block';
                document.getElementById('quiz-content').style.display = 'none';
                document.getElementById('quiz-error').style.display = 'none';

                // Load Quiz Info
                const qResponse = await fetch(`${API_URL}/quizzes/${quizTakeId}`);
                if (!qResponse.ok) throw new Error('Failed to load quiz');
                const quizInfo = await qResponse.json();
                
                document.getElementById('quiz-title').innerText = quizInfo.title;
                document.getElementById('category-badge').innerText = quizInfo.category;
                timeLeft = quizInfo.timer * 60;
                totalTime = timeLeft;

                // Load Questions
                const response = await fetch(`${API_URL}/quizzes/${quizTakeId}/questions`);
                if (!response.ok) throw new Error('Failed to load questions');
                currentQuestions = await response.json();
                
                if (currentQuestions.length === 0) {
                    throw new Error('This quiz has no questions.');
                }

                document.getElementById('total-q-num').innerText = currentQuestions.length;

                // Success: Hide loading, show content
                document.getElementById('quiz-loading').style.display = 'none';
                document.getElementById('quiz-content').style.display = 'grid';

                renderQuestion();
                initTimerCircle();
                startTimer();
                renderNavigator();
            } catch (err) {
                console.error(err);
                document.getElementById('quiz-loading').style.display = 'none';
                document.getElementById('quiz-content').style.display = 'none';
                document.getElementById('quiz-error').style.display = 'block';
                if (err.message) {
                    document.querySelector('#quiz-error p').innerText = err.message;
                }
            }
        }

        function renderQuestion() {
            const q = currentQuestions[currentIndex];
            const card = document.getElementById('question-card');
            
            // 1. Data Validation: Ensure all necessary data exists
            if (!q || !q.question_text || !q.option_a || !q.option_b || !q.option_c || !q.option_d) {
                card.innerHTML = `
                    <div class="empty-state glass p-5 text-center">
                        <i class="fas fa-exclamation-triangle empty-illustration text-danger"></i>
                        <h2>Question data is incomplete.</h2>
                        <p class="mb-4">This question cannot be displayed due to missing information.</p>
                        <a href="quiz-list.html" class="btn btn-primary">Return to Quiz List</a>
                    </div>
                `;
                return;
            }

            // Animation reset
            card.style.animation = 'none';
            card.offsetHeight; // trigger reflow
            card.style.animation = null;

            document.getElementById('current-q-num').innerText = currentIndex + 1;
            document.getElementById('question-text').innerText = q.question_text;

            renderNavigator();

            const optionsContainer = document.getElementById('options-container');
            optionsContainer.innerHTML = '';
            
            const options = [
                { key: 'A', text: q.option_a },
                { key: 'B', text: q.option_b },
                { key: 'C', text: q.option_c },
                { key: 'D', text: q.option_d }
            ];

            options.forEach(opt => {
                const btn = document.createElement('button');
                btn.className = `option-btn ${userAnswers[q.id] === opt.key ? 'selected' : ''}`;
                
                // 2. Fixed Display: Ensure option text is rendered properly
                const optionText = opt.text || "Option data unavailable";
                
                btn.innerHTML = `
                    <div class="custom-radio"></div>
                    <div class="opt-content">
                        <span class="opt-key mr-2">${opt.key}.</span>
                        <span class="opt-text">${optionText}</span>
                    </div>
                `;
                btn.onclick = () => {
                    userAnswers[q.id] = opt.key;
                    renderQuestion();
                    updateProgress();
                    renderNavigator();
                };
                optionsContainer.appendChild(btn);
            });

            document.getElementById('prev-btn').disabled = currentIndex === 0;
            if (currentIndex === currentQuestions.length - 1) {
                document.getElementById('next-btn').style.display = 'none';
                document.getElementById('submit-quiz-btn').style.display = 'inline-flex';
            } else {
                document.getElementById('next-btn').style.display = 'inline-flex';
                document.getElementById('submit-quiz-btn').style.display = 'none';
            }
        }

        function renderNavigator() {
            const nav = document.getElementById('question-navigator');
            nav.innerHTML = '';
            currentQuestions.forEach((q, i) => {
                const dot = document.createElement('div');
                dot.className = `nav-dot ${i === currentIndex ? 'active' : ''} ${userAnswers[q.id] ? 'answered' : ''}`;
                dot.innerText = i + 1;
                dot.onclick = () => { currentIndex = i; renderQuestion(); };
                nav.appendChild(dot);
            });
        }

        function initTimerCircle() {
            const circle = document.getElementById('timer-progress');
            if (circle) {
                const radius = circle.r.baseVal.value;
                const circumference = radius * 2 * Math.PI;
                circle.style.strokeDasharray = `${circumference} ${circumference}`;
                circle.style.strokeDashoffset = 0;
            }
        }

        function setTimerProgress(percent) {
            const circle = document.getElementById('timer-progress');
            if (circle) {
                const radius = circle.r.baseVal.value;
                const circumference = radius * 2 * Math.PI;
                const offset = circumference - (percent / 100 * circumference);
                circle.style.strokeDashoffset = offset;
            }
        }

        function startTimer() {
            timerInterval = setInterval(() => {
                timeLeft--;
                const mins = Math.floor(timeLeft / 60);
                const secs = timeLeft % 60;
                document.getElementById('quiz-timer').innerText = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
                
                const percent = (timeLeft / totalTime) * 100;
                setTimerProgress(percent);

                if (timeLeft <= 0) {
                    clearInterval(timerInterval);
                    submitQuiz();
                }
            }, 1000);
        }

        function updateProgress() {
            const answered = Object.keys(userAnswers).length;
            const percent = Math.round((answered / currentQuestions.length) * 100);
            document.getElementById('progress-bar').style.width = `${percent}%`;
            document.getElementById('progress-percent').innerText = percent;
        }

        async function submitQuiz() {
            clearInterval(timerInterval);
            const answersArray = Object.keys(userAnswers).map(qId => ({
                question_id: parseInt(qId),
                selected_option: userAnswers[qId]
            }));

            const submitBtn = document.getElementById('submit-quiz-btn');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';

            try {
                const response = await fetch(`${API_URL}/attempts/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${auth.getToken()}`
                    },
                    body: JSON.stringify({
                        quiz_id: parseInt(quizTakeId),
                        answers: answersArray
                    })
                });

                if (response.ok) {
                    const result = await response.json();
                    localStorage.setItem('last_result', JSON.stringify(result));
                    window.location.href = 'result.html';
                }
            } catch (err) {
                console.error(err);
            }
        }

        document.getElementById('next-btn').onclick = () => {
            if (currentIndex < currentQuestions.length - 1) {
                currentIndex++;
                renderQuestion();
            }
        };

        document.getElementById('prev-btn').onclick = () => {
            if (currentIndex > 0) {
                currentIndex--;
                renderQuestion();
            }
        };

        document.getElementById('submit-quiz-btn').onclick = submitQuiz;
        document.getElementById('quit-quiz-btn').onclick = () => {
            if(confirm('Are you sure you want to quit? Your progress will be lost.')) {
                window.location.href = 'quiz-list.html';
            }
        };

        startQuiz();
    }

    // 5. RESULT PAGE LOGIC ENHANCED
    if (document.getElementById('score-percent')) {
        const result = JSON.parse(localStorage.getItem('last_result'));
        if (result) {
            const percent = Math.round(result.percentage);
            
            // Animate Score Ring
            setTimeout(() => {
                const circle = document.getElementById('score-progress');
                const radius = circle.r.baseVal.value;
                const circumference = radius * 2 * Math.PI;
                circle.style.strokeDasharray = `${circumference} ${circumference}`;
                const offset = circumference - (percent / 100 * circumference);
                circle.style.strokeDashoffset = offset;
                
                // Animate Number
                animateValue('score-percent', 0, percent, 1500);
            }, 100);

            document.getElementById('res-correct').innerText = result.score;
            document.getElementById('res-total').innerText = Math.round(result.score / (result.percentage / 100)) || 0;
            document.getElementById('res-wrong').innerText = (document.getElementById('res-total').innerText - result.score) || 0;
            
            const badge = document.getElementById('performance-badge');
            if (percent >= 80) {
                badge.innerText = '🏆 Excellent Master';
                badge.className = 'badge badge-lg bg-success text-white';
                launchConfetti();
            } else if (percent >= 60) {
                badge.innerText = '🌟 Great Job';
                badge.className = 'badge badge-lg bg-primary text-white';
            } else {
                badge.innerText = '📚 Keep Learning';
                badge.className = 'badge badge-lg bg-warning text-white';
            }
        }
    }

    function animateValue(id, start, end, duration) {
        const obj = document.getElementById(id);
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            obj.innerHTML = Math.floor(progress * (end - start) + start) + "%";
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    function launchConfetti() {
        const duration = 3 * 1000;
        const animationEnd = Date.now() + duration;
        const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

        const randomInRange = (min, max) => Math.random() * (max - min) + min;

        const interval = setInterval(function() {
            const timeLeft = animationEnd - Date.now();

            if (timeLeft <= 0) {
                return clearInterval(interval);
            }

            const particleCount = 50 * (timeLeft / duration);
            confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } }));
            confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } }));
        }, 250);
    }
});

    // 4. QUIZ LIST LOGIC
    const quizListContainer = document.getElementById('quiz-list-container');
    const searchInput = document.getElementById('search-quiz');
    const catFilter = document.getElementById('filter-category');
    const diffFilter = document.getElementById('filter-difficulty');

    async function loadQuizzes() {
        if (!quizListContainer) return;

        const params = new URLSearchParams();
        if (searchInput?.value) params.append('search', searchInput.value);
        if (catFilter?.value) params.append('category', catFilter.value);
        if (diffFilter?.value) params.append('difficulty', diffFilter.value);

        try {
            const response = await fetch(`${API_URL}/quizzes/?${params.toString()}`);
            const quizzes = await response.json();

            quizListContainer.innerHTML = '';
            if (quizzes.length === 0) {
                quizListContainer.innerHTML = `
                    <div class="empty-state glass p-5 w-full text-center" style="grid-column: 1 / -1;">
                        <i class="fas fa-search empty-illustration"></i>
                        <p>No quizzes found matching your criteria.</p>
                    </div>
                `;
                return;
            }

            quizzes.forEach((quiz, index) => {
                const card = document.createElement('div');
                card.className = 'quiz-card glass fade-in';
                card.setAttribute('data-aos', 'fade-up');
                card.setAttribute('data-aos-delay', index * 50);
                card.innerHTML = `
                    <h3>${quiz.title}</h3>
                    <p class="text-muted small mb-4">${quiz.description || 'Challenge yourself with this community quiz.'}</p>
                    <div class="card-meta-row">
                        <span class="card-meta-badge"><i class="fas fa-tag"></i> ${quiz.category}</span>
                        <span class="card-meta-badge"><i class="fas fa-signal"></i> ${quiz.difficulty}</span>
                        <span class="card-meta-badge"><i class="fas fa-clock"></i> ${quiz.timer}m</span>
                        <span class="card-meta-badge"><i class="fas fa-user"></i> ${quiz.creator_name}</span>
                    </div>
                    <div class="card-actions-grid d-flex gap-2">
                        <button class="btn btn-primary flex-1" onclick="checkAuthAndRedirect('take-quiz.html?id=${quiz.id}')">
                            Start Quiz
                        </button>
                        <button class="btn btn-secondary" onclick="window.location.href='quiz-details.html?id=${quiz.id}'">
                            Details
                        </button>
                    </div>
                `;
                quizListContainer.appendChild(card);
            });
        } catch (err) {
            console.error(err);
        }
    }

    if (quizListContainer) {
        [searchInput, catFilter, diffFilter].forEach(el => {
            el?.addEventListener('input', loadQuizzes);
        });
        loadQuizzes();
    }

    window.checkAuthAndRedirect = (url) => {
        if (!auth.isLoggedIn()) {
            showAuthModal("You must login before viewing quiz details or attempting a quiz.");
        } else {
            window.location.href = url;
        }
    };
