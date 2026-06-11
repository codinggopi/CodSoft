# QuizSphere – Full Stack Online Quiz Maker

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Architecture](#architecture)
5. [Database Schema](#database-schema)
6. [API Endpoints](#api-endpoints)
7. [Frontend Pages](#frontend-pages)
8. [How to Run](#how-to-run)
9. [Deployment Guide](#deployment-guide)
10. [Future Enhancements](#future-enhancements)

---

## 🎯 Project Overview

**QuizSphere** is a production-ready, full-stack online quiz maker web application. It allows users to create interactive quizzes, participate in quizzes created by others, and view detailed results and global leaderboards. The platform is designed with a modern, responsive UI and a robust, secure backend.

**Project Name:** QuizSphere  
**Type:** Full Stack Web Application  
**Purpose:** Online Quiz Creation, Management, and Participation Platform  
**Target Users:** Students, Educators, Quiz Enthusiasts, Corporate Trainers

---

## ✨ Features

### 1. User Authentication & Management
- **User Registration** – Create an account with name, email, and strong password
- **User Login** – Secure JWT-based authentication
- **User Logout** – Clear session and secure redirection
- **Profile Management** – Edit full name, email, bio, and avatar
- **Avatar Upload** – Upload profile pictures (stored as base64/data URLs)
- **Password Strength Meter** – Real-time visual feedback on password strength
- **Protected Routes** – Route guards prevent unauthorized access to dashboard, profile, and quiz pages

### 2. Quiz Creation & Management
- **Quiz Builder** – Multi-step form to create quizzes with:
  - Title, description, category, and difficulty level
  - Custom timer (in minutes)
  - Unlimited Multiple Choice Questions (MCQs)
- **Question Builder** – Dynamic form to add/edit questions with:
  - Question text
  - Four options (A, B, C, D)
  - Correct answer selector
- **Quiz Editing** – Edit your own quizzes after creation
- **Quiz Deletion** – Delete quizzes you created
- **My Quizzes Dashboard** – View and manage all your created quizzes

### 3. Quiz Taking Experience
- **Interactive Quiz Interface** – One question at a time with smooth navigation
- **Question Navigator** – Visual dot-based navigator to jump between questions
- **Progress Tracker** – Real-time progress bar and percentage indicator
- **Countdown Timer** – Circular timer with auto-submission on expiration
- **Answer Review** – Mark questions as answered with visual indicators
- **Previous/Next Navigation** – Move freely between questions
- **Quiz Quit Confirmation** – Warns user before abandoning progress

### 4. Results & Analytics
- **Score Summary** – Total questions, correct/wrong answers, and percentage score
- **Performance Badges** – Dynamic feedback based on score:
  - 🏆 Excellent Master (80%+)
  - 🌟 Great Job (60-79%)
  - 📚 Keep Learning (<60%)
- **Animated Score Ring** – SVG circular progress animation on result page
- **Confetti Celebration** – Visual celebration for high scores
- **Attempt History** – View past performance with dates and scores in dashboard

### 5. Social & Discovery
- **Global Leaderboard** – Top 10 rankings with podium display for top 3
- **Search & Filter** – Find quizzes by:
  - Title search
  - Category filter (Java, Python, Web Development, Data Structures, Algorithms, Machine Learning)
  - Difficulty filter (Easy, Medium, Hard)
- **Sort Options** – Newest first or most popular
- **Quiz Categories** – Browse quizzes across 10+ tech categories

### 6. UI/UX Features
- **Responsive Design** – Fully optimized for Mobile, Tablet, and Desktop
- **Dark Mode** – Persistent theme selection with localStorage
- **Glassmorphism Design** – Modern glass-effect cards and elements
- **Smooth Animations** – AOS (Animate On Scroll) library integration
- **Loading Skeletons** – Skeleton loaders for better perceived performance
- **Toast Notifications** – Non-intrusive success/error messages
- **Modal Dialogs** – Authentication prompts for protected actions
- **Sticky Navbar** – Navbar changes style on scroll

---

## 🛠️ Tech Stack

### Frontend
| Technology | Purpose |
|------------|---------|
| **HTML5** | Semantic page structure |
| **CSS3** | Modern styling with custom properties, flexbox, grid |
| **Vanilla JavaScript (ES6+)** | Dynamic functionality without heavy frameworks |
| **AOS Library** | Scroll-based animations |
| **Font Awesome 6** | Icon library |
| **Canvas Confetti** | Celebration effects on high scores |

### Backend
| Technology | Purpose |
|------------|---------|
| **Python 3.x** | Programming language |
| **FastAPI** | High-performance asynchronous web framework |
| **SQLAlchemy** | ORM for database interaction |
| **Pydantic** | Data validation and settings management |
| **python-jose** | JWT token generation and validation |
| **passlib[bcrypt]** | Password hashing |
| **python-dotenv** | Environment variable management |
| **uvicorn** | ASGI server |

### Database
| Technology | Purpose |
|------------|---------|
| **MySQL 8.0** | Relational database for permanent data persistence |

---

## 🏗️ Architecture

### System Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                        QuizSphere Platform                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐      ┌───────────┐  │
│  │   Browser    │─────▶│   FastAPI    │─────▶│   MySQL   │  │
│  │  (Frontend)  │◀─────│   Backend    │◀─────│ Database  │  │
│  └──────────────┘      └──────────────┘      └───────────┘  │
│        │                      │                     │        │
│        │   HTML/CSS/JS        │   Python/REST API   │        │
│        │   (Vanilla JS)       │   (Async/SQLAlchemy)│        │
│        │                      │                     │        │
│        ▼                      ▼                     ▼        │
│  ┌──────────────┐      ┌──────────────┐      ┌───────────┐  │
│  │   index.html │      │   main.py    │      │  users    │  │
│  │  login.html  │      │   routers/   │      │  quizzes  │  │
│  │  dashboard   │      │   models/    │      │ questions │  │
│  │  quiz-list   │      │   schemas/   │      │ attempts  │  │
│  │  take-quiz   │      │   auth/      │      │           │  │
│  │  result      │      │   database/  │      │           │  │
│  └──────────────┘      └──────────────┘      └───────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Backend Structure
```
quizsphere/backend/
├── .env                          # Environment variables (not in git)
├── requirements.txt              # Python dependencies
└── app/
    ├── main.py                   # FastAPI app entry point, CORS, routers
    ├── auth/
    │   └── auth.py               # JWT creation, password hashing
    ├── database/
    │   └── db.py                 # SQLAlchemy engine, session, base
    ├── models/
    │   └── models.py             # SQLAlchemy ORM models (User, Quiz, Question, Attempt)
    ├── routers/
    │   ├── auth.py               # /auth/* endpoints (register, login, profile)
    │   ├── quizzes.py            # /quizzes/* endpoints (CRUD)
    │   ├── attempts.py           # /attempts/* endpoints (submit, history)
    │   ├── leaderboard.py        # /leaderboard/* endpoints
    │   └── users.py              # /users/* endpoints (stats, my-quizzes)
    └── schemas/
        └── schemas.py            # Pydantic models for request/response validation
```

### Frontend Structure
```
quizsphere/frontend/
├── index.html                    # Home page with hero section
├── login.html                    # Login page
├── register.html                 # Registration page
├── dashboard.html                # User dashboard with stats and my quizzes
├── profile.html                  # User profile with attempt history
├── edit-profile.html             # Edit profile form with avatar upload
├── quiz-list.html                # Browse/search/filter quizzes
├── quiz-details.html             # Quiz details before taking
├── take-quiz.html                # Interactive quiz taking interface
├── create-quiz.html              # Multi-step quiz creation form
├── result.html                   # Quiz results with score animation
├── leaderboard.html              # Global leaderboard with podium
├── css/
│   ├── style.css                 # Main stylesheet (35KB+)
│   └── darkmode.css              # Dark mode styles
├── js/
│   ├── auth.js                   # Authentication logic, UI initialization
│   ├── quiz.js                   # Quiz creation, taking, and result logic
│   ├── profile.js                # Profile and dashboard data loading
│   └── leaderboard.js            # Leaderboard rendering
└── assets/                       # Static assets (images, etc.)
```

---

## 🗄️ Database Schema

### Entity Relationship Diagram
```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    users    │       │   quizzes   │       │  questions  │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id (PK)     │◀──────│ creator_id  │       │ quiz_id (FK)│
│ full_name   │       │ id (PK)     │──────▶│ id (PK)     │
│ email       │       │ title       │       │ question_text│
│ password_hash│      │ description │       │ option_a    │
│ avatar_url  │       │ category    │       │ option_b    │
│ bio         │       │ difficulty  │       │ option_c    │
│ created_at  │       │ timer       │       │ option_d    │
└─────────────┘       │ created_at  │       │ correct_ans │
                      └─────────────┘       └─────────────┘
                             │                     │
                             │                     │
                             ▼                     ▼
                      ┌─────────────┐       ┌─────────────┐
                      │  attempts   │       │             │
                      ├─────────────┤       │             │
                      │ id (PK)     │       │             │
                      │ user_id (FK)│◀──────│             │
                      │ quiz_id (FK)│──────▶│             │
                      │ score       │       │             │
                      │ percentage  │       │             │
                      │ attempted_at│       │             │
                      └─────────────┘       │             │
                                            │             │
                                            └─────────────┘
```

### Table Definitions

#### users
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier |
| full_name | VARCHAR(255) | NOT NULL | User's full name |
| email | VARCHAR(255) | UNIQUE, NOT NULL, INDEXED | User's email address |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt-hashed password |
| avatar_url | VARCHAR(500) | NULL | Profile picture URL or base64 data |
| bio | TEXT | NULL | User biography/description |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |

#### quizzes
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique quiz identifier |
| title | VARCHAR(255) | NOT NULL | Quiz title |
| description | TEXT | NULL | Quiz description |
| category | VARCHAR(100) | NULL | Quiz category (e.g., Python, Java) |
| difficulty | VARCHAR(50) | NULL | Difficulty level (Easy, Medium, Hard) |
| timer | INT | NULL | Duration in minutes |
| creator_id | INT | FOREIGN KEY → users(id) | Quiz creator's user ID |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Quiz creation timestamp |

#### questions
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique question identifier |
| quiz_id | INT | FOREIGN KEY → quizzes(id) | Parent quiz ID |
| question_text | TEXT | NOT NULL | The question content |
| option_a | VARCHAR(255) | NOT NULL | First answer option |
| option_b | VARCHAR(255) | NOT NULL | Second answer option |
| option_c | VARCHAR(255) | NOT NULL | Third answer option |
| option_d | VARCHAR(255) | NOT NULL | Fourth answer option |
| correct_answer | CHAR(1) | NOT NULL | Correct option (A, B, C, or D) |

#### attempts
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique attempt identifier |
| user_id | INT | FOREIGN KEY → users(id) | User who took the quiz |
| quiz_id | INT | FOREIGN KEY → quizzes(id) | Quiz that was attempted |
| score | INT | NULL | Number of correct answers |
| percentage | FLOAT | NULL | Score percentage |
| attempted_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | When the quiz was taken |

---

## 🔌 API Endpoints

### Authentication (`/auth`)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/login` | Login and get JWT token | No |
| GET | `/auth/me` | Get current user profile | Yes |
| PUT | `/auth/me` | Update user profile | Yes |

### Quizzes (`/quizzes`)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/quizzes/` | Create a new quiz | Yes |
| GET | `/quizzes/` | Get all quizzes (with filters) | No |
| GET | `/quizzes/{quiz_id}` | Get a specific quiz | No |
| GET | `/quizzes/{quiz_id}/questions` | Get questions for a quiz | No |
| PUT | `/quizzes/{quiz_id}` | Update a quiz | Yes (owner only) |
| DELETE | `/quizzes/{quiz_id}` | Delete a quiz | Yes (owner only) |

### Attempts (`/attempts`)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/attempts/` | Submit quiz answers | Yes |
| GET | `/attempts/history` | Get user's attempt history | Yes |
| GET | `/attempts/{attempt_id}` | Get specific attempt details | No |

### Leaderboard (`/leaderboard`)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/leaderboard/` | Get top 10 global rankings | No |

### Users (`/users`)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/users/stats` | Get user statistics | Yes |
| GET | `/users/my-quizzes` | Get current user's quizzes | Yes |

---

## 🖥️ Frontend Pages

### 1. Home Page (`index.html`)
- Hero section with animated floating cards
- Call-to-action buttons for creating and taking quizzes
- Statistics section with animated counters
- Feature highlights
- Responsive navigation with auth state awareness

### 2. Login Page (`login.html`)
- Clean login form with email and password
- Password visibility toggle
- Error message display for failed logins
- Redirect support after login
- Link to registration page

### 3. Register Page (`register.html`)
- Full name, email, password, and confirm password fields
- Real-time password strength meter
- Password visibility toggle
- Form validation
- Link to login page

### 4. Dashboard (`dashboard.html`)
- Welcome message with user's first name
- Stats cards: quizzes created, attempted, average score, highest score
- "My Quizzes" section with edit/delete actions
- Recent attempts table
- Quick access to create new quiz

### 5. Profile Page (`profile.html`)
- Large avatar display with fallback initial
- User info: name, email, bio, join date
- Stats overview (same as dashboard)
- Recent activity table with attempt history
- Achievements section
- Link to edit profile

### 6. Edit Profile (`edit-profile.html`)
- Avatar upload with preview
- Remove avatar option
- Edit full name, email, and bio
- Save changes with loading state
- Cancel button to return to profile

### 7. Browse Quizzes (`quiz-list.html`)
- Search bar for title/creator/topic search
- Category filter dropdown
- Difficulty filter dropdown
- Sort by newest or most popular
- Responsive quiz card grid
- Loading skeletons

### 8. Quiz Details (`quiz-details.html`)
- Quiz information display
- Category and difficulty badges
- Question count
- Timer display
- Start quiz button

### 9. Take Quiz (`take-quiz.html`)
- Quiz header with title, category badge, and timer
- Circular countdown timer with SVG progress ring
- Question display with four option buttons
- Question navigator (dot grid)
- Progress bar
- Previous/Next/Submit buttons
- Quit confirmation dialog
- Auto-submit on timer expiration

### 10. Create Quiz (`create-quiz.html`)
- Multi-step form (3 steps + review):
  1. Quiz details (title, description, category, difficulty, timer)
  2. Question builder (add unlimited MCQs)
  3. Review and publish
- Stepper indicator
- Dynamic question card addition/removal
- Form validation at each step

### 11. Result Page (`result.html`)
- Animated score ring (SVG circular progress)
- Score percentage with count-up animation
- Correct/wrong answer counts
- Performance badge with dynamic styling
- Confetti celebration for high scores
- Retry or browse more quizzes

### 12. Leaderboard (`leaderboard.html`)
- Podium display for top 3 performers
- Rank badges and avatars
- Table for ranks 4-10
- Empty state message when no data

---

## 🚀 How to Run

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- pip (Python package manager)

### Step 1: Database Setup
1. Open MySQL client (Workbench, CLI, or phpMyAdmin)
2. Create the database and tables:
   ```sql
   SOURCE quizsphere/database_schema.sql;
   ```
3. Or run the migration if tables already exist:
   ```sql
   USE quizsphere;
   ALTER TABLE users ADD COLUMN avatar_url VARCHAR(500) NULL;
   ALTER TABLE users ADD COLUMN bio TEXT NULL;
   ```

### Step 2: Backend Setup
1. Navigate to the backend folder:
   ```bash
   cd quizsphere/backend
   ```
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # OR
   source venv/bin/activate  # Mac/Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment:
   - Create a `.env` file based on `.env.example`
   - Update `DATABASE_URL` with your MySQL credentials:
     ```
     DATABASE_URL=mysql://root:root@localhost:3306/quizsphere
     SECRET_KEY=your-secure-secret-key-here
     ALGORITHM=HS256
     ACCESS_TOKEN_EXPIRE_MINUTES=1440
     ```
5. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
6. API will be available at `http://localhost:8000`
7. Auto-generated docs at `http://localhost:8000/docs`

### Step 3: Frontend Setup
1. Simply open `quizsphere/frontend/index.html` in any modern web browser
2. Ensure the backend is running at `http://localhost:8000`
3. No build step required – pure HTML/CSS/JS

---

## 🌐 Deployment Guide

### Frontend Deployment
| Platform | Steps |
|----------|-------|
| **GitHub Pages** | Push `frontend/` folder to a GitHub repo, enable Pages in settings |
| **Netlify** | Drag and drop the `frontend/` folder or connect Git repo |
| **Vercel** | Import project, set root directory to `frontend/` |
| **Cloudflare Pages** | Connect Git repo, build command not needed (static site) |

**Note:** Update `API_URL` in `js/auth.js` and `js/quiz.js` to point to your deployed backend URL.

### Backend Deployment
| Platform | Steps |
|----------|-------|
| **Render** | Connect Git repo, set build command `pip install -r requirements.txt`, start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Railway** | Connect Git repo, add MySQL plugin, set environment variables |
| **Vercel** | Use `vercel.json` configuration for Python/FastAPI |
| **Python Anywhere** | Upload files, set up virtualenv, configure WSGI file |

### Database Deployment
| Service | Notes |
|---------|-------|
| **Railway MySQL** | Free tier available, auto-backups |
| **Aiven MySQL** | Managed MySQL with monitoring |
| **AWS RDS** | Production-grade managed database |
| **Google Cloud SQL** | Fully managed MySQL service |

### Environment Variables for Production
```env
# Database
DATABASE_URL=mysql://user:password@host:3306/quizsphere

# JWT Security (GENERATE A STRONG RANDOM KEY!)
SECRET_KEY=generate-with-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS (Update with your frontend domain)
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

---

## 🔒 Security Considerations

### Implemented
- JWT-based authentication with secure password hashing (bcrypt)
- Protected API routes with dependency injection
- CORS configuration (to be restricted in production)
- SQL injection prevention via SQLAlchemy ORM
- Input validation via Pydantic schemas

### Recommended for Production
1. **Generate a strong SECRET_KEY:**
   ```bash
   openssl rand -hex 32
   ```
2. **Restrict CORS origins** to your actual frontend domain
3. **Add rate limiting** to prevent brute-force attacks
4. **Implement password reset** functionality
5. **Add email verification** for new accounts
6. **Use HTTPS** in production
7. **Add request logging** and monitoring
8. **Implement CSRF protection** for state-changing operations
9. **Add input sanitization** for rich text fields
10. **Regular security audits** and dependency updates

---

## 🧪 Testing Checklist

### Functional Testing
- [ ] User registration with valid/invalid data
- [ ] User login with correct/incorrect credentials
- [ ] Profile update (name, email, bio, avatar)
- [ ] Quiz creation with multiple questions
- [ ] Quiz editing and deletion
- [ ] Quiz taking with timer
- [ ] Quiz submission and result display
- [ ] Leaderboard display
- [ ] Search and filter functionality
- [ ] Dark mode toggle
- [ ] Responsive design on mobile/tablet/desktop

### Security Testing
- [ ] JWT token expiration handling
- [ ] Unauthorized access to protected routes
- [ ] SQL injection attempts
- [ ] XSS attempts in quiz content
- [ ] Password strength enforcement

---

## 📈 Future Enhancements

### Short Term
- [ ] Password reset via email
- [ ] Email verification for new accounts
- [ ] Quiz sharing via link
- [ ] Quiz categories management
- [ ] Quiz difficulty auto-calculation
- [ ] User achievements and badges system
- [ ] Quiz bookmarking/favorites

### Medium Term
- [ ] Real-time multiplayer quizzes
- [ ] Quiz templates library
- [ ] Image support in questions
- [ ] Audio questions support
- [ ] Time-per-question tracking
- [ ] Detailed analytics for quiz creators
- [ ] Social sharing of results

### Long Term
- [ ] AI-powered quiz generation
- [ ] Team/group quizzes
- [ ] Certification upon completion
- [ ] Integration with LMS platforms
- [ ] Mobile app (React Native/Flutter)
- [ ] Advanced reporting and insights
- [ ] Monetization features (premium quizzes)

---

## 👤 Author

**Gopinath G**  
CodSoft Web Development Intern (June 2026)  
Project: Level 2 Task 2 – Full Stack Online Quiz Maker

---

## 📄 License

This project is created for educational purposes as part of the CodSoft Internship program.

---

*Last Updated: June 2026*
