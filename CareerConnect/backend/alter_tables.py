import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./careerconnect.db"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        conn.execute("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE;")
        conn.execute("UPDATE users SET is_active = TRUE;")
        print("Added is_active to users.")
except Exception as e:
    print("Users alter failed (may already exist):", e)

try:
    with engine.connect() as conn:
        conn.execute("ALTER TABLE companies ADD COLUMN status VARCHAR DEFAULT 'Active';")
        conn.execute("UPDATE companies SET status = 'Active';")
        print("Added status to companies.")
except Exception as e:
    print("Companies alter failed (may already exist):", e)
