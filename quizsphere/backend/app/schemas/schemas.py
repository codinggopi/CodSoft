from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    avatar_url: Optional[str] = None
    bio: Optional[str] = None

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

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

class QuestionBase(BaseModel):
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    id: int
    quiz_id: int

    class Config:
        from_attributes = True

class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    difficulty: str
    timer: int

class QuizCreate(QuizBase):
    questions: List[QuestionCreate]

class QuizUpdate(QuizBase):
    questions: Optional[List[QuestionCreate]] = None

class QuizResponse(QuizBase):
    id: int
    creator_id: int
    created_at: datetime
    creator_name: Optional[str] = None
    question_count: Optional[int] = 0

    class Config:
        from_attributes = True

class AttemptBase(BaseModel):
    quiz_id: int
    score: int
    percentage: float

class AttemptCreate(BaseModel):
    quiz_id: int
    answers: List[dict]

class AttemptResponse(AttemptBase):
    id: int
    user_id: int
    attempted_at: datetime
    quiz_title: Optional[str] = None

    class Config:
        from_attributes = True

class LeaderboardEntry(BaseModel):
    rank: int
    user_name: str
    quiz_name: str
    score: int
    percentage: float
