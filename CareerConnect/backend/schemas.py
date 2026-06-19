from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str

class UserCreate(UserBase):
    password: str
    security_question: str
    security_answer: str
    company_name: Optional[str] = None
    company_email: Optional[EmailStr] = None
    industry: Optional[str] = None
    website: Optional[str] = None

class VerifyEmailRequest(BaseModel):
    email: EmailStr

class VerifyAnswerRequest(BaseModel):
    email: EmailStr
    answer: str

class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str

class ResetPasswordRequest(BaseModel):
    reset_token: str
    new_password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class JobBase(BaseModel):
    title: str
    company: str
    location: str
    salary: str
    job_type: str
    description: str
    requirements: str
    skills: str
    deadline: Optional[str] = None

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: int
    employer_id: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class ApplicationBase(BaseModel):
    job_id: int
    cover_letter: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationResponse(ApplicationBase):
    id: int
    candidate_id: int
    resume_path: str
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class CompanyBase(BaseModel):
    name: str
    logo_url: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    location: Optional[str] = None
    founded_year: Optional[str] = None
    website: Optional[str] = None
    linkedin: Optional[str] = None
    mission: Optional[str] = None
    vision: Optional[str] = None
    benefits: Optional[str] = None
    description: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: int
    employer_id: int
    created_at: datetime
    class Config:
        from_attributes = True

class InterviewBase(BaseModel):
    application_id: int
    scheduled_time: datetime
    meeting_link: Optional[str] = None
    notes: Optional[str] = None

class InterviewCreate(InterviewBase):
    pass

class InterviewResponse(InterviewBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class NotificationBase(BaseModel):
    title: str
    message: str

class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    created_at: datetime
    class Config:
        from_attributes = True

class ProfileViewResponse(BaseModel):
    id: int
    employer_id: int
    candidate_id: int
    created_at: datetime
    class Config:
        from_attributes = True
