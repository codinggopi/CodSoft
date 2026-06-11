from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.db import get_db
from models import models
from schemas import schemas
from routers.auth import get_current_user

router = APIRouter(prefix="/attempts", tags=["Attempts"])

@router.post("/", response_model=schemas.AttemptResponse)
def submit_quiz(
    attempt_data: schemas.AttemptCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == attempt_data.quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    total_questions = len(quiz.questions)
    correct_answers = 0
    
    # Map questions for faster lookup
    questions_map = {q.id: q.correct_answer for q in quiz.questions}
    
    for ans in attempt_data.answers:
        q_id = ans.get("question_id")
        selected = ans.get("selected_option")
        if q_id in questions_map and questions_map[q_id] == selected:
            correct_answers += 1
            
    percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    new_attempt = models.Attempt(
        user_id=current_user.id,
        quiz_id=quiz.id,
        score=correct_answers,
        percentage=percentage
    )
    
    db.add(new_attempt)
    db.commit()
    db.refresh(new_attempt)
    
    new_attempt.quiz_title = quiz.title
    return new_attempt

@router.get("/history", response_model=List[schemas.AttemptResponse])
def get_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    attempts = db.query(models.Attempt).filter(models.Attempt.user_id == current_user.id).order_by(models.Attempt.attempted_at.desc()).all()
    for a in attempts:
        a.quiz_title = a.quiz.title
    return attempts

@router.get("/{attempt_id}", response_model=schemas.AttemptResponse)
def get_attempt(attempt_id: int, db: Session = Depends(get_db)):
    attempt = db.query(models.Attempt).filter(models.Attempt.id == attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    attempt.quiz_title = attempt.quiz.title
    return attempt
