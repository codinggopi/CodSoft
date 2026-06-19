from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models, database, auth
from database import engine, get_db

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CareerConnect API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes import users, jobs, applications, companies

app.include_router(users.router)
app.include_router(jobs.router)
app.include_router(applications.router)
app.include_router(companies.router)


# Seed DB data on startup
@app.on_event("startup")
def seed_data():
    db = next(get_db())
    admin_email = "admin@careerconnect.com"
    employer_email = "employer@careerconnect.com"
    candidate_email = "candidate@careerconnect.com"
    
    if not db.query(models.User).filter(models.User.email == admin_email).first():
        db.add(models.User(name="Admin User", email=admin_email, password=auth.get_password_hash("Admin@123"), role="admin"))
    if not db.query(models.User).filter(models.User.email == employer_email).first():
        db.add(models.User(name="Employer User", email=employer_email, password=auth.get_password_hash("Employer@123"), role="employer"))
    if not db.query(models.User).filter(models.User.email == candidate_email).first():
        db.add(models.User(name="Candidate User", email=candidate_email, password=auth.get_password_hash("Candidate@123"), role="candidate"))
    db.commit()

@app.get("/")
def read_root():
    return {"message": "Welcome to CareerConnect API"}
