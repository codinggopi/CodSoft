from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect
from database.db import engine, Base
from routers import auth, quizzes, attempts, leaderboard, users
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="QuizSphere API", version="1.0.0")

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    
    required_user_columns = {"avatar_url", "bio"}
    inspector = inspect(engine)
    try:
        columns = {col["name"] for col in inspector.get_columns("users")}
        missing = required_user_columns - columns
        if missing:
            logger.warning(
                "Database schema is outdated. Missing columns in 'users' table: %s. "
                "Please run the migration statements in database_schema.sql.",
                ", ".join(sorted(missing)),
            )
        else:
            logger.info("Database schema validation passed. All required columns present.")
    except Exception as exc:
        logger.error("Schema validation failed: %s", exc)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(quizzes.router)
app.include_router(attempts.router)
app.include_router(leaderboard.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to QuizSphere API"}
