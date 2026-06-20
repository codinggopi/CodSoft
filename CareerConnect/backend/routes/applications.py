
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import models, schemas, database
from routes.users import get_current_user
import cloudinary
import cloudinary.uploader
from cloudinary_config import *

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.post("/apply", response_model=schemas.ApplicationResponse)
async def apply_for_job(
    job_id: int = Form(...),
    cover_letter: Optional[str] = Form(None),
    resume: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "candidate":
        raise HTTPException(status_code=403, detail="Only candidates can apply for jobs")

    # Check if job exists
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Check if already applied
    existing_app = db.query(models.Application).filter(
        models.Application.job_id == job_id,
        models.Application.candidate_id == current_user.id
    ).first()
    if existing_app:
        raise HTTPException(status_code=400, detail="You have already applied for this job")

    # Handle file upload
    file_ext = resume.filename.split(".")[-1].lower()
    if file_ext not in ["pdf", "doc", "docx"]:
        raise HTTPException(status_code=400, detail="Only PDF, DOC, and DOCX files are allowed")

    # Upload resume to Cloudinary
    try:
        upload_result = cloudinary.uploader.upload(
            resume.file,
            folder="careerconnect/resumes",
            resource_type="auto"
        )
        resume_url = upload_result.get("secure_url")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload resume: {e}")


    new_app = models.Application(
        job_id=job_id,
        candidate_id=current_user.id,
        resume_url=resume_url,
        cover_letter=cover_letter
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)

    # Simulated email
    print(f"Application Submitted Email sent to {current_user.email}")
    return new_app

@router.get("/", response_model=List[schemas.ApplicationResponse])
def get_applications(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role == "candidate":
        # Candidate sees their own apps
        apps = db.query(models.Application).filter(models.Application.candidate_id == current_user.id).all()
        return apps
    elif current_user.role == "employer":
        # Employer sees apps for their jobs
        jobs = db.query(models.Job.id).filter(models.Job.employer_id == current_user.id).subquery()
        apps = db.query(models.Application).filter(models.Application.job_id.in_(jobs)).all()
        return apps
    elif current_user.role == "admin":
        return db.query(models.Application).all()
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")

@router.put("/status/{app_id}", response_model=schemas.ApplicationResponse)
def update_application_status(
    app_id: int,
    status_update: str = Form(...), # 'Accepted' or 'Rejected'
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    app = db.query(models.Application).filter(models.Application.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    job = db.query(models.Job).filter(models.Job.id == app.job_id).first()

    if current_user.role != "admin" and (current_user.role != "employer" or job.employer_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to update this application")

    app.status = status_update
    db.commit()
    db.refresh(app)
    return app
