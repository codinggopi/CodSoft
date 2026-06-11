# CodSoft Web Development Internship - Level 2 Task 2

## Project Title: QuizSphere – Full Stack Online Quiz Maker

QuizSphere is a complete production-ready Full Stack Online Quiz Maker web application. It allows users to create quizzes, participate in quizzes created by others, and view detailed results and leaderboards.

---

## 🚀 Tech Stack

### Frontend
- **HTML5 & CSS3**: Modern, semantic structure and styling.
- **Vanilla JavaScript**: Pure JS for dynamic functionality without heavy frameworks.
- **Responsive Design**: Fully optimized for Mobile, Tablet, and Desktop.
- **Dark Mode**: Persistent theme selection for better user experience.

### Backend
- **Python FastAPI**: High-performance asynchronous web framework.
- **JWT Authentication**: Secure session management and protected routes.
- **SQLAlchemy ORM**: Database interaction and management.
- **Pydantic**: Robust data validation and settings management.

### Database
- **MySQL**: Relational database for permanent data persistence.

---

## ✨ Features

### User Authentication
- ✅ **Register**: Create an account with name, email, and strong password.
- ✅ **Login**: Secure access with JWT token generation.
- ✅ **Logout**: Clear session and secure redirection.

### Quiz Creation
- ✅ **Quiz Builder**: Title, description, category, difficulty, and timer.
- ✅ **Questions**: Add unlimited Multiple Choice Questions (MCQs).
- ✅ **Management**: Edit and Delete your own quizzes.

### Quiz Taking
- ✅ **Interactive UI**: One question at a time with "Next" and "Previous" navigation.
- ✅ **Timer**: Countdown timer with auto-submission on expiration.
- ✅ **Progress Tracker**: Visual progress bar and question navigator.

### Results & Analytics
- ✅ **Score Summary**: Total questions, correct/wrong answers, and percentage.
- ✅ **Performance Status**: Feedback based on score (Excellent, Good, etc.).
- ✅ **Attempt History**: View your past performance in the dashboard.

### Social & Discovery
- ✅ **Leaderboard**: Global Top 10 rankings.
- ✅ **Search & Filter**: Find quizzes by title, category, or difficulty.
- ✅ **Categories**: Browse quizzes across 10+ tech categories (Java, Python, Web Dev, etc.).

---

## 📂 Project Structure

```text
quizsphere/
├── backend/                # FastAPI Backend
│   ├── app/
│   │   ├── auth/          # JWT & Security logic
│   │   ├── database/      # MySQL connection setup
│   │   ├── models/        # SQLAlchemy database models
│   │   ├── routers/       # API endpoints (Users, Quizzes, Attempts, etc.)
│   │   ├── schemas/       # Pydantic data validation models
│   │   └── main.py        # Application entry point
│   ├── .env.example       # Environment variables template
│   └── requirements.txt   # Backend dependencies
├── frontend/               # Vanilla JS Frontend
│   ├── css/               # Stylesheets (including dark mode)
│   ├── js/                # Frontend logic (Auth, Quiz, Profile, Leaderboard)
│   └── *.html             # Application pages
├── database_schema.sql     # Complete MySQL schema script
└── README.md               # Project-specific documentation
```

---

## 🛠️ Local Setup

### 1. Database Setup
1. Open your MySQL client.
2. Run the commands in [database_schema.sql](file:///c:/Users/Gopinath%20G/Desktop/CodSoft/quizsphere/database_schema.sql) to create the tables.

### 2. Backend Setup
1. Navigate to the backend folder:
   ```bash
   cd quizsphere/backend
   ```
2. Install dependencies directly:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment:
   - Create a `.env` file based on `.env.example`.
   - Update `DATABASE_URL` with your MySQL credentials.
5. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

### 3. Frontend Setup
1. Simply open [index.html](file:///c:/Users/Gopinath%20G/Desktop/CodSoft/quizsphere/frontend/index.html) in any modern web browser.
2. Ensure the backend is running at `http://localhost:8000`.

---

## 🌐 Deployment

- **Frontend**: Deploy the `frontend/` folder to **GitHub Pages**, **Netlify**, or **Vercel**.
- **Backend**: Deploy the `backend/` folder to **Render**, **Railway**, or **Vercel**.
- **Database**: Use a managed MySQL service like **Railway MySQL** or **Aiven**.

---

## 👤 Author
**Gopinath G**  
CodSoft Web Development Intern (June 2026)
