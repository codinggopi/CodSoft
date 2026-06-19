from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas, database
from routes.users import get_current_user

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.get("/", response_model=List[schemas.JobResponse])
def get_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    jobs = db.query(models.Job).offset(skip).limit(limit).all()
    return jobs

@router.get("/{job_id}", response_model=schemas.JobResponse)
def get_job(job_id: int, db: Session = Depends(database.get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/", response_model=schemas.JobResponse)
def create_job(job: schemas.JobCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "employer" and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to post jobs")
    new_job = models.Job(**job.dict(), employer_id=current_user.id)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.put("/{job_id}", response_model=schemas.JobResponse)
def update_job(job_id: int, job_update: schemas.JobCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.employer_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update this job")
    
    for key, value in job_update.dict().items():
        setattr(job, key, value)
    db.commit()
    db.refresh(job)
    return job

@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.employer_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete this job")
    
    db.delete(job)
    db.commit()
    return {"detail": "Job deleted successfully"}
