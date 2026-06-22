
import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from sqlalchemy.orm import Session

import models
import database
import auth
from database import engine, get_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_db_and_tables():
    try:
        logger.info("Creating database tables...")
        models.Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")

app = FastAPI(title="CareerConnect API")

import os

FRONTEND_URL = os.getenv("FRONTEND_URL", "https://careerconnect-online.netlify.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes import users, jobs, applications, companies

app.include_router(users.router)
app.include_router(jobs.router)
app.include_router(applications.router)
app.include_router(companies.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
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
def health():
    return {
        "status": "success",
        "message": "CareerConnect API Running Successfully"
    }

@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)
