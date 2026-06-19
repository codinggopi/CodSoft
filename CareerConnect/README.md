# CareerConnect – Professional Job Board Portal

CareerConnect is a modern, responsive, and secure full-stack Job Board Portal developed for the **CodSoft Internship Level 2 Task 1**.

The platform connects employers and job seekers through a professional web application. Employers can seamlessly create and manage job postings, while candidates can search for jobs, upload resumes, and apply online.

## ✨ Key Features
- **Modern UI/UX**: Clean layout, glassmorphism card effects, gradient buttons, and responsive design for mobile, tablet, and desktop.
- **Dark Mode**: Fully supported dark/light themes with local storage persistence.
- **Role-Based Authentication**: Secure JWT authentication and bcrypt password hashing for Candidates, Employers, and Admins.
- **Job Management**: Employers can post, edit, and delete jobs. Candidates can perform advanced searches and filter jobs.
- **Resume Upload**: Candidates can upload resumes (PDF, DOC, DOCX) directly to the server.
- **Dedicated Dashboards**: Custom views and statistics for tracking applications, jobs, and system-wide analytics.
- **Password Toggle**: Integrated eye-icon toggle to easily show/hide passwords on all auth forms.

## 🛠️ Technology Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript, Font Awesome Icons.
- **Backend**: Python FastAPI, SQLite database.
- **Libraries/Tools**: SQLAlchemy (ORM), Pydantic (Data validation), python-jose (JWT), passlib (bcrypt password hashing), python-multipart (File uploads).

---

## 🚀 Setup Instructions

### 1. Backend Setup
The backend does not include a pre-built virtual environment to keep the project lightweight. You will need to create one and install the requirements:

1. Open a terminal and navigate to the project root directory.

2. Install the required dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Start the backend FastAPI server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
   *The backend API will start running at `http://127.0.0.1:8000`.*

### 2. Frontend Setup
1. Simply open the `frontend/index.html` file in your web browser.
2. Alternatively, serve the `frontend` directory using a local development server (like VS Code's **Live Server** extension) for the best experience.
3. The frontend utilizes vanilla JavaScript `fetch` to communicate directly with the running FastAPI backend.

---

## 🔐 Demo Accounts
The SQLite database automatically seeds the following accounts on startup. You can use these to test the various dashboards:

| Role | Email | Password |
|------|-------|----------|
| **Admin** | `admin@careerconnect.com` | `Admin@123` |
| **Employer** | `employer@careerconnect.com` | `Employer@123` |
| **Candidate** | `candidate@careerconnect.com` | `Candidate@123` |

---

## 📂 Folder Structure
```text
CareerConnect/
│
├── frontend/
│   ├── index.html, login.html, register.html, ...
│   ├── assets/
│   │   ├── css/style.css
│   │   └── js/app.js, auth.js, theme.js, jobs.js
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── requirements.txt
│   ├── routes/
│   │   ├── users.py
│   │   ├── jobs.py
│   │   └── applications.py
│   └── uploads/ (Created automatically on first resume upload)
│
└── README.md
```

## 📝 License
This project was built for the CodSoft Internship program. Feel free to explore, modify, and improve it.
