# CareerConnect – Professional Job Board Portal

CareerConnect is a modern, responsive, and secure full-stack Job Board Portal developed for the **CodSoft Internship Level 2 Task 1**.

The platform connects employers and job seekers through a professional web application. Employers can seamlessly create and manage job postings, while candidates can search for jobs, upload resumes, and apply online.

## ✨ Key Features
- **Modern UI/UX**: Clean layout, glassmorphism card effects, gradient buttons, and responsive design for mobile, tablet, and desktop.
- **Dark Mode**: Fully supported dark/light themes with local storage persistence.
- **Role-Based Authentication**: Secure JWT authentication and bcrypt password hashing for Candidates, Employers, and Admins.
- **Job Management**: Employers can post, edit, and delete jobs. Candidates can perform advanced searches and filter jobs.
- **Cloud File Uploads**: Integrated with Cloudinary for seamless Profile Picture and Resume (PDF, DOC, DOCX) uploads.
- **Dedicated Dashboards**: Custom views and statistics for tracking applications, jobs, and system-wide analytics.
- **Password Toggle**: Integrated eye-icon toggle to easily show/hide passwords on all auth forms.

## 🛠️ Technology Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript, Font Awesome Icons. Hosted on **Netlify**.
- **Backend**: Python FastAPI. Hosted on **Vercel**.
- **Database**: PostgreSQL (managed via **Supabase**).
- **Libraries/Tools**: SQLAlchemy (ORM), Pydantic (Data validation), python-jose (JWT), passlib (bcrypt password hashing), python-multipart (File uploads), Cloudinary SDK.

---

## 🚀 Live Demo & Deployment

- **Frontend Application**: [https://careerconnect-online.netlify.app](https://careerconnect-online.netlify.app)
- **Backend API Docs**: [https://careerconnect-navy.vercel.app/docs](https://careerconnect-navy.vercel.app/docs)

*(Note: The backend is hosted on Vercel's serverless infrastructure, which might take a few seconds to warm up on the first request.)*

---

## 💻 Local Setup Instructions

### 1. Database Setup
The project is configured to use PostgreSQL. You can use a local PostgreSQL instance or a cloud provider like Supabase.

### 2. Backend Setup
1. Open a terminal and navigate to the `backend` directory.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file and fill in your database and Cloudinary credentials:
   ```env
   DATABASE_URL="postgresql://user:password@host:port/dbname"
   SECRET_KEY="your_super_secret_jwt_key"
   CLOUDINARY_CLOUD_NAME="your_cloud_name"
   CLOUDINARY_API_KEY="your_api_key"
   CLOUDINARY_API_SECRET="your_api_secret"
   FRONTEND_URL="http://127.0.0.1:5500"
   BACKEND_URL="http://localhost:8000"
   ```
4. Start the backend FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

### 3. Frontend Setup
1. Open the `frontend` directory in VS Code.
2. Use the **Live Server** extension to serve the files (usually starts on port 5500).
3. The frontend utilizes vanilla JavaScript `fetch` to communicate directly with the FastAPI backend.

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
│   ├── cloudinary_config.py
│   ├── requirements.txt
│   ├── .env.example
│   └── routes/
│       ├── users.py
│       ├── jobs.py
│       └── applications.py
│
└── README.md
```

## 📝 License
This project was built for the CodSoft Internship program. Feel free to explore, modify, and improve it.
