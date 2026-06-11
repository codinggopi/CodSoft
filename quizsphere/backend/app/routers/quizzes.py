from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database.db import get_db
from models import models
from schemas import schemas
from auth import get_current_user

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])

@router.post("/", response_model=schemas.QuizResponse)
def create_quiz(
    quiz: schemas.QuizCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_quiz = models.Quiz(
        title=quiz.title,
        description=quiz.description,
        category=quiz.category,
        difficulty=quiz.difficulty,
        timer=quiz.timer,
        creator_id=current_user.id
    )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)

    for q in quiz.questions:
        new_question = models.Question(
            quiz_id=new_quiz.id,
            question_text=q.question_text,
            option_a=q.option_a,
            option_b=q.option_b,
            option_c=q.option_c,
            option_d=q.option_d,
            correct_answer=q.correct_answer
        )
        db.add(new_question)
    
    db.commit()
    db.refresh(new_quiz)
    return new_quiz

@router.get("/", response_model=List[schemas.QuizResponse])
def get_quizzes(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Quiz)
    if category:
        query = query.filter(models.Quiz.category == category)
    if difficulty:
        query = query.filter(models.Quiz.difficulty == difficulty)
    if search:
        query = query.filter(models.Quiz.title.contains(search))
    
    quizzes = query.all()
    
    # Enrich with creator name and question count
    for q in quizzes:
        q.creator_name = q.creator.full_name
        q.question_count = len(q.questions)
        
    return quizzes

@router.get("/{quiz_id}", response_model=schemas.QuizResponse)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    quiz.creator_name = quiz.creator.full_name
    quiz.question_count = len(quiz.questions)
    return quiz

@router.get("/{quiz_id}/questions", response_model=List[schemas.QuestionResponse])
def get_quiz_questions(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz.questions

@router.put("/{quiz_id}", response_model=schemas.QuizResponse)
def update_quiz(
    quiz_id: int,
    quiz_update: schemas.QuizUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    if db_quiz.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this quiz")
    
    for key, value in quiz_update.dict().items():
        setattr(db_quiz, key, value)
    
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

@router.delete("/{quiz_id}")
def delete_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    if db_quiz.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this quiz")
    
    db.delete(db_quiz)
    db.commit()
    return {"message": "Quiz deleted successfully"}
