# QuizSphere – Full Stack Online Quiz Maker

QuizSphere is a comprehensive, production-ready full-stack web application designed for creating, taking, and managing interactive online quizzes. It was developed as part of the **CodSoft Web Development Internship (Level 2 Task 2)**.

## ✨ Key Features

- **Robust User Authentication**: Secure registration, login, and session management powered by JSON Web Tokens (JWT) and bcrypt hashing.
- **Dynamic Quiz Builder**: Educators and users can easily construct complex quizzes featuring unlimited multiple-choice questions, custom categories, dynamic timers, and difficulty settings.
- **Interactive Quiz Taking Experience**: A clean, distraction-free interface showing one question at a time, complete with progress tracking, visual feedback, and auto-submission when the timer expires.
- **Comprehensive Analytics & Dashboards**: Instant post-quiz scoring, performance grading (e.g., Excellent, Needs Improvement), and a personal history dashboard.
- **Global Leaderboards**: Real-time Top 10 global rankings to foster competition among users.
- **Modern UI & UX**: Fully responsive layout optimized for Mobile, Tablet, and Desktop displays, featuring a persistent system-wide dark mode toggle.

## 🛠️ Technology Stack

- **Frontend Environment**: HTML5, CSS3, Vanilla JavaScript
- **Backend Framework**: Python FastAPI (Asynchronous, high-performance)
- **Database System**: MySQL (Relational data persistence)
- **Object-Relational Mapping (ORM)**: SQLAlchemy
- **Data Validation & Settings**: Pydantic
- **Security**: JWT (python-jose), Password Hashing (passlib)

---

## 📂 Project Structure

```text
quizsphere/
├── backend/                # FastAPI Application Code
│   ├── app/
│   │   ├── auth/          # JWT handling and security logic
│   │   ├── database/      # MySQL engine configuration
│   │   ├── models/        # SQLAlchemy database tables
│   │   ├── routers/       # RESTful API Endpoints
│   │   ├── schemas/       # Pydantic data validation schemas
│   │   └── main.py        # FastAPI entry point
│   ├── requirements.txt   # Python package dependencies
│   └── .env.example       # Example environment variables
│
├── frontend/               # Client-Side Application
│   ├── css/               # Modular stylesheets and Dark Mode logic
│   ├── js/                # Vanilla JS controllers (Auth, Quiz, Profile)
│   └── *.html             # HTML Views
│
├── database_schema.sql     # Complete MySQL initialization script
└── README.md               # Project documentation
```

---

## 🚀 Local Setup Instructions

### 1. Database Setup
1. Launch your local or remote MySQL client.
2. Execute the commands provided in `database_schema.sql` to initialize the database and construct the necessary tables.

### 2. Backend Setup
1. Open your terminal and navigate to the `backend` folder:
   ```bash
   cd quizsphere/backend
   ```
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on `.env.example` and update your MySQL connection string (`DATABASE_URL`).
4. Start the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload
   ```
   *(The server will run at `http://localhost:8000`)*

### 3. Frontend Setup
1. Open the `frontend` directory in VS Code or your preferred editor.
2. Serve the directory using a local development server (like VS Code's **Live Server** extension) or simply open the `index.html` file in any modern web browser.
3. Ensure the backend is running so the frontend can fetch API data successfully.

---

## 🌐 Deployment Guidelines

This project is structured to be easily deployed to modern cloud hosting providers:

- **Database**: Use managed MySQL services like **Railway**, **Aiven**, or **AWS RDS**.
- **Backend API**: Deploy the FastAPI application to serverless or containerized platforms such as **Render**, **Vercel**, or **Railway**.
- **Frontend App**: Host the static assets on **GitHub Pages**, **Netlify**, or **Vercel**. Don't forget to update the `API_URL` variable in your frontend JavaScript configuration to point to the live backend domain!

---

## 👤 Author
**Gopinath G**  
CodSoft Web Development Intern (June 2026)
