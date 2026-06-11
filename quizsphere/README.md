# QuizSphere – Full Stack Online Quiz Maker

QuizSphere is a production-ready, full-stack web application that allows users to create, participate in, and manage quizzes. Built for the CodSoft Web Development Internship (Level 2 Task 2).

## Tech Stack

- **Frontend:** HTML5, CSS3, Vanilla JavaScript (Modern, Responsive, Dark Mode)
- **Backend:** Python FastAPI
- **Database:** MySQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT (JSON Web Tokens)
- **Validation:** Pydantic

## Features

- **User Authentication:** Secure Register, Login, and Logout with JWT.
- **Quiz Creation:** Create quizzes with unlimited multiple-choice questions, categories, and timers.
- **Quiz Taking:** Interactive quiz interface with one question at a time, progress tracking, and auto-submission.
- **Dashboard:** Personal statistics, quiz history, and management of created quizzes.
- **Leaderboard:** Global rankings based on quiz performance.
- **Dark Mode:** System-wide theme toggle with persistent user preference.
- **Responsive Design:** Optimized for Mobile, Tablet, and Desktop.

## Project Structure

```
quizsphere/
├── backend/                # FastAPI Backend
│   ├── app/
│   │   ├── auth/          # JWT & Hashing
│   │   ├── database/      # DB Connection
│   │   ├── models/        # SQLAlchemy Models
│   │   ├── routers/       # API Endpoints
│   │   ├── schemas/       # Pydantic Schemas
│   │   └── main.py        # Entry Point
│   ├── requirements.txt
│   └── .env.example
├── frontend/               # Vanilla JS Frontend
│   ├── css/               # Styling & Dark Mode
│   ├── js/                # Logic (Auth, Quiz, Profile)
│   └── *.html             # Pages
└── database_schema.sql     # MySQL Schema
```

## Setup Instructions

### Backend Setup
1. Navigate to the `backend` folder.
2. Install dependencies directly: `pip install -r requirements.txt`.
3. Create a `.env` file from `.env.example` and update your MySQL connection string.
4. Run the server: `uvicorn app.main:app --reload`.

### Frontend Setup
1. Open any HTML file (e.g., `index.html`) in a browser.
2. Ensure the backend is running at `http://localhost:8000`.

## Deployment Guide

### Backend (Render / Vercel)
1. Push the `backend` folder to a GitHub repository.
2. Connect the repository to **Render** or **Vercel**.
3. Set Environment Variables: `DATABASE_URL`, `SECRET_KEY`, etc.
4. Set Build Command: `pip install -r requirements.txt`.
5. Set Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.

### Database (Railway / Aiven)
1. Create a MySQL instance on **Railway**.
2. Run the `database_schema.sql` script to initialize tables.
3. Copy the Connection URL to the backend environment variables.

### Frontend (GitHub Pages / Netlify)
1. Push the `frontend` folder to GitHub.
2. Deploy using **GitHub Pages** or **Netlify**.
3. Update `API_URL` in `js/auth.js` to point to your deployed backend.

## Author
**Gopinath G** - CodSoft Web Development Intern
