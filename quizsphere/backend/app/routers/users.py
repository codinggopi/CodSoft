from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from ..database.db import get_db
from ..models import models
from ..schemas import schemas
from .auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/stats")
def get_user_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    quizzes_created = db.query(models.Quiz).filter(models.Quiz.creator_id == current_user.id).count()
    quizzes_attempted = db.query(models.Attempt).filter(models.Attempt.user_id == current_user.id).count()
    
    avg_score_query = db.query(func.avg(models.Attempt.percentage)).filter(models.Attempt.user_id == current_user.id).scalar()
    avg_score = round(float(avg_score_query), 2) if avg_score_query else 0
    
    max_score_query = db.query(func.max(models.Attempt.percentage)).filter(models.Attempt.user_id == current_user.id).scalar()
    max_score = round(float(max_score_query), 2) if max_score_query else 0
    
    return {
        "quizzes_created": quizzes_created,
        "quizzes_attempted": quizzes_attempted,
        "average_score": avg_score,
        "highest_score": max_score
    }

@router.get("/my-quizzes", response_model=list[schemas.QuizResponse])
def get_my_quizzes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    quizzes = db.query(models.Quiz).filter(models.Quiz.creator_id == current_user.id).all()
    for q in quizzes:
        q.creator_name = current_user.full_name
        q.question_count = len(q.questions)
    return quizzes
