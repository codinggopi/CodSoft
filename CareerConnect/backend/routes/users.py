from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import models, schemas, auth, database
import random
import time
import uuid
import re

# In-memory OTP and Reset Store
otp_store = {}


router = APIRouter(prefix="/users", tags=["Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except auth.JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    hashed_answer = auth.get_password_hash(user.security_answer.strip().lower())
    new_user = models.User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        role=user.role,
        password=hashed_password,
        security_question=user.security_question,
        security_answer=hashed_answer
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if user.role == "employer":
        new_company = models.Company(
            employer_id=new_user.id,
            name=user.company_name or f"{user.name}'s Company",
            industry=user.industry,
            website=user.website
        )
        db.add(new_company)
        db.commit()

    # Simulated email notification here
    print(f"Registration Success Email sent to {user.email}")
    return new_user

@router.post("/login", response_model=schemas.Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.post("/forgot-password/verify-email")
def forgot_password_verify_email(req: schemas.VerifyEmailRequest, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    if not user.security_question:
        raise HTTPException(status_code=400, detail="User has no security question set")
    return {"message": "Email verified", "security_question": user.security_question}

@router.post("/forgot-password/verify-answer")
def forgot_password_verify_answer(req: schemas.VerifyAnswerRequest, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    
    if not auth.verify_password(req.answer.strip().lower(), user.security_answer):
        raise HTTPException(status_code=401, detail="Incorrect security answer")
    
    reset_token = str(uuid.uuid4())
    otp_store[req.email] = {
        "otp": "CAPTCHA_BYPASS",
        "expires_at": time.time() + 300, # 5 minutes
        "attempts": 0,
        "reset_token": reset_token
    }
    
    return {"message": "Answer verified", "reset_token": reset_token}

@router.post("/forgot-password/verify-otp")
def forgot_password_verify_otp(req: schemas.VerifyOTPRequest):
    if req.email not in otp_store:
        raise HTTPException(status_code=400, detail="OTP session not found or expired")
    
    session = otp_store[req.email]
    
    if time.time() > session["expires_at"]:
        del otp_store[req.email]
        raise HTTPException(status_code=400, detail="OTP expired")
    
    if session["attempts"] >= 3:
        del otp_store[req.email]
        raise HTTPException(status_code=403, detail="Too many invalid attempts. Session locked out.")
    
    if session["otp"] != req.otp:
        session["attempts"] += 1
        raise HTTPException(status_code=401, detail="Invalid OTP")
    
    reset_token = str(uuid.uuid4())
    session["reset_token"] = reset_token
    
    return {"message": "OTP verified", "reset_token": reset_token}

@router.post("/forgot-password/reset")
def forgot_password_reset(req: schemas.ResetPasswordRequest, db: Session = Depends(database.get_db)):
    # Find email by reset_token
    email_to_reset = None
    for em, session in otp_store.items():
        if session.get("reset_token") == req.reset_token:
            email_to_reset = em
            break
            
    if not email_to_reset:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
        
    session = otp_store[email_to_reset]
    if time.time() > session["expires_at"]:
        del otp_store[email_to_reset]
        raise HTTPException(status_code=400, detail="Reset session expired")
    
    # Validate complexity
    pwd = req.new_password
    if len(pwd) < 8 or not re.search(r"[a-z]", pwd) or not re.search(r"[A-Z]", pwd) or not re.search(r"\d", pwd) or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd):
        raise HTTPException(status_code=400, detail="Password does not meet complexity requirements")
        
    user = db.query(models.User).filter(models.User.email == email_to_reset).first()
    user.password = auth.get_password_hash(pwd)
    db.commit()
    
    del otp_store[email_to_reset]
    return {"message": "Password successfully reset"}

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(current_user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    # Cascading deletes
    if current_user.role == 'employer':
        # Delete applications to all jobs posted by this employer
        jobs = db.query(models.Job).filter(models.Job.employer_id == current_user.id).all()
        job_ids = [job.id for job in jobs]
        if job_ids:
            db.query(models.Application).filter(models.Application.job_id.in_(job_ids)).delete(synchronize_session=False)
        # Delete the jobs themselves
        db.query(models.Job).filter(models.Job.employer_id == current_user.id).delete(synchronize_session=False)
    
    # Delete applications by this candidate
    db.query(models.Application).filter(models.Application.candidate_id == current_user.id).delete(synchronize_session=False)
    
    # Finally, delete the user
    db.query(models.User).filter(models.User.id == current_user.id).delete(synchronize_session=False)
    
    db.commit()
    return None
