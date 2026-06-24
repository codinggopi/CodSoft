from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models, schemas, database
from routes.users import get_current_user

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.get("/me", response_model=schemas.CompanyResponse)
def get_my_company(current_user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    if current_user.role != 'employer':
        raise HTTPException(status_code=403, detail="Only employers have a company profile")
        
    company = db.query(models.Company).filter(models.Company.employer_id == current_user.id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company profile not found")
        
    return company

@router.put("/me", response_model=schemas.CompanyResponse)
def update_my_company(company_update: schemas.CompanyCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    if current_user.role != 'employer':
        raise HTTPException(status_code=403, detail="Only employers have a company profile")
        
    company = db.query(models.Company).filter(models.Company.employer_id == current_user.id).first()
    if not company:
        # Create one if it somehow doesn't exist
        company = models.Company(employer_id=current_user.id)
        db.add(company)
        
    for key, value in company_update.dict().items():
        setattr(company, key, value)
        
    db.commit()
    db.refresh(company)
    return company

@router.get("/{company_id}", response_model=schemas.CompanyResponse)
def get_company(company_id: int, db: Session = Depends(database.get_db)):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.get("/employer/{employer_id}", response_model=schemas.CompanyResponse)
def get_company_by_employer(employer_id: int, db: Session = Depends(database.get_db)):
    company = db.query(models.Company).filter(models.Company.employer_id == employer_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company profile not found for this employer")
    return company
