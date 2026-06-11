from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database.db import get_db
from models import models
from schemas import schemas

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])

@router.get("/", response_model=List[schemas.LeaderboardEntry])
def get_leaderboard(db: Session = Depends(get_db)):
    top_attempts = db.query(models.Attempt).order_by(models.Attempt.percentage.desc()).limit(10).all()
    
    leaderboard = []
    for i, attempt in enumerate(top_attempts):
        leaderboard.append(schemas.LeaderboardEntry(
            rank=i + 1,
            user_name=attempt.user.full_name,
            quiz_name=attempt.quiz.title,
            score=attempt.score,
            percentage=attempt.percentage
        ))
    
    return leaderboard
