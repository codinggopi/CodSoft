from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

import models, schemas, database, auth
from routes.users import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])

def verify_admin(current_user: models.User = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user

@router.get("/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(database.get_db), admin: models.User = Depends(verify_admin)):
    total_users = db.query(models.User).count()
    total_candidates = db.query(models.User).filter(models.User.role == 'candidate').count()
    total_employers = db.query(models.User).filter(models.User.role == 'employer').count()
    total_admins = db.query(models.User).filter(models.User.role == 'admin').count()
    
    total_companies = db.query(models.Company).count()
    
    total_jobs = db.query(models.Job).count()
    active_jobs = db.query(models.Job).filter(models.Job.status == 'Active').count()
    closed_jobs = db.query(models.Job).filter(models.Job.status != 'Active').count()
    
    total_applications = db.query(models.Application).count()
    pending_applications = db.query(models.Application).filter(models.Application.status == 'Pending').count()
    accepted_applications = db.query(models.Application).filter(models.Application.status == 'Accepted').count()
    rejected_applications = db.query(models.Application).filter(models.Application.status == 'Rejected').count()

    return {
        "total_users": total_users,
        "total_candidates": total_candidates,
        "total_employers": total_employers,
        "total_admins": total_admins,
        "total_companies": total_companies,
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "closed_jobs": closed_jobs,
        "total_applications": total_applications,
        "pending_applications": pending_applications,
        "accepted_applications": accepted_applications,
        "rejected_applications": rejected_applications
    }

@router.get("/recent-users")
def get_recent_users(db: Session = Depends(database.get_db), admin: models.User = Depends(verify_admin)):
    recent_users = db.query(models.User).order_by(models.User.id.desc()).limit(10).all()
    return [{"id": u.id, "name": u.name, "email": u.email, "role": u.role, "created_at": u.created_at} for u in recent_users]

@router.get("/user-demographics")
def get_user_demographics(db: Session = Depends(database.get_db), admin: models.User = Depends(verify_admin)):
    candidates = db.query(models.User).filter(models.User.role == 'candidate').count()
    employers = db.query(models.User).filter(models.User.role == 'employer').count()
    admins = db.query(models.User).filter(models.User.role == 'admin').count()
    return {
        "candidates": candidates,
        "employers": employers,
        "admins": admins
    }

@router.get("/application-stats")
def get_application_stats(db: Session = Depends(database.get_db), admin: models.User = Depends(verify_admin)):
    # Standard DB statuses are Pending, Accepted, Rejected. 
    # The requirement asks for Applied, Under Review, Shortlisted, Accepted, Rejected.
    # We will map 'Pending' to 'Applied' for the UI, and if the DB ever gets 'Under Review' or 'Shortlisted', it captures them.
    applied = db.query(models.Application).filter(models.Application.status == 'Pending').count()
    under_review = db.query(models.Application).filter(models.Application.status == 'Under Review').count()
    shortlisted = db.query(models.Application).filter(models.Application.status == 'Shortlisted').count()
    accepted = db.query(models.Application).filter(models.Application.status == 'Accepted').count()
    rejected = db.query(models.Application).filter(models.Application.status == 'Rejected').count()
    
    return {
        "Applied": applied,
        "Under Review": under_review,
        "Shortlisted": shortlisted,
        "Accepted": accepted,
        "Rejected": rejected
    }

@router.get("/users")
def get_all_users(db: Session = Depends(database.get_db), admin: models.User = Depends(verify_admin)):
    users = db.query(models.User).all()
    return [{"id": u.id, "name": u.name, "email": u.email, "phone": u.phone, "role": u.role, "is_active": getattr(u, 'is_active', True), "created_at": u.created_at} for u in users]

@router.put("/users/{user_id}/status")
def update_user_status(user_id: int, status_update: dict, db: Session = Depends(database.get_db), admin: models.User = Depends(verify_admin)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if "is_active" in status_update:
        user.is_active = status_update["is_active"]
    db.commit()
    return {"message": "User status updated", "is_active": user.is_active}

@router.put("/users/{user_id}/profile")
def update_user_profile_admin(user_id: int, profile_data: dict, db: Session = Depends(database.get_db), admin: models.User = Depends(verify_admin)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update simple fields
    for key in ["name", "email", "phone", "role"]:
        if key in profile_data:
            setattr(user, key, profile_data[key])
            
    db.commit()
    return {"message": "User profile updated"}

@router.delete("/users/{user_id}")
def delete_user_by_admin(user_id: int, db: Session = Depends(database.get_db), admin: models.User = Depends(verify_admin)):
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own admin account here")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        db.delete(user)
        db.commit()
        return {"message": "User permanently deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/companies")
def get_all_companies(db: Session = Depends(database.get_db), admin: models.User = Depends(verify_admin)):
    companies = db.query(models.Company).all()
    return [{"id": c.id, "name": c.name, "industry": c.industry, "status": getattr(c, 'status', 'Active'), "employer_id": c.employer_id} for c in companies]

@router.put("/companies/{company_id}/status")
def update_company_status(company_id: int, status_update: dict, db: Session = Depends(database.get_db), admin: models.User = Depends(verify_admin)):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    if "status" in status_update:
        company.status = status_update["status"]
    db.commit()
    return {"message": "Company status updated", "status": company.status}

@router.delete("/companies/{company_id}")
def delete_company_admin(company_id: int, db: Session = Depends(database.get_db), admin: models.User = Depends(verify_admin)):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    try:
        # If the company has an employer, we delete the employer.
        # Due to SQLAlchemy cascades (User -> Jobs -> Applications -> Interviews),
        # deleting the employer will wipe all dependencies.
        if company.employer_id:
            employer = db.query(models.User).filter(models.User.id == company.employer_id).first()
            if employer:
                db.delete(employer)
        
        # Then delete the company itself
        db.delete(company)
        db.commit()
        return {"message": "Company and all dependent records permanently deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/jobs")
def get_all_jobs(db: Session = Depends(database.get_db), admin: models.User = Depends(verify_admin)):
    jobs = db.query(models.Job).all()
    return [{"id": j.id, "title": j.title, "company": j.company, "status": j.status, "created_at": j.created_at, "employer_id": j.employer_id} for j in jobs]

@router.delete("/jobs/{job_id}")
def delete_job_admin(job_id: int, db: Session = Depends(database.get_db), admin: models.User = Depends(verify_admin)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job: raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"message": "Job deleted"}

@router.put("/jobs/{job_id}/status")
def update_job_status_admin(job_id: int, status_data: dict, db: Session = Depends(database.get_db), admin: models.User = Depends(verify_admin)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job: raise HTTPException(status_code=404, detail="Job not found")
    if "status" in status_data: job.status = status_data["status"]
    db.commit()
    return {"message": "Job status updated"}

@router.get("/applications")
def get_all_applications(db: Session = Depends(database.get_db), admin: models.User = Depends(verify_admin)):
    apps = db.query(models.Application).all()
    res = []
    for app in apps:
        job = db.query(models.Job).filter(models.Job.id == app.job_id).first()
        candidate = db.query(models.User).filter(models.User.id == app.candidate_id).first()
        res.append({
            "id": app.id,
            "status": app.status,
            "resume_url": app.resume_url,
            "created_at": app.created_at,
            "job_title": job.title if job else "Unknown",
            "company": job.company if job else "Unknown",
            "candidate_name": candidate.name if candidate else "Unknown"
        })
    return res

@router.delete("/applications/{app_id}")
def delete_app_admin(app_id: int, db: Session = Depends(database.get_db), admin: models.User = Depends(verify_admin)):
    app = db.query(models.Application).filter(models.Application.id == app_id).first()
    if not app: raise HTTPException(status_code=404, detail="Application not found")
    db.delete(app)
    db.commit()
    return {"message": "Application deleted"}

@router.put("/applications/{app_id}/status")
def update_app_status_admin(app_id: int, status_data: dict, db: Session = Depends(database.get_db), admin: models.User = Depends(verify_admin)):
    app = db.query(models.Application).filter(models.Application.id == app_id).first()
    if not app: raise HTTPException(status_code=404, detail="Application not found")
    if "status" in status_data: app.status = status_data["status"]
    db.commit()
    return {"message": "Application status updated"}
