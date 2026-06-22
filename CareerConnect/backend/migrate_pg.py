import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def migrate_pg():
    if not DATABASE_URL or DATABASE_URL.startswith("sqlite"):
        print("This script is for PostgreSQL migration only.")
        return

    print("Connecting to PostgreSQL Database...")
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN oauth_provider VARCHAR;"))
            print("Added oauth_provider column.")
        except Exception as e:
            print("oauth_provider column might already exist:", e)

        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN oauth_id VARCHAR;"))
            print("Added oauth_id column.")
        except Exception as e:
            print("oauth_id column might already exist:", e)

        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN profile_picture VARCHAR;"))
            print("Added profile_picture column.")
        except Exception as e:
            print("profile_picture column might already exist:", e)

        try:
            # We also need to alter password, security_question, and security_answer to be nullable for OAuth users
            conn.execute(text("ALTER TABLE users ALTER COLUMN password DROP NOT NULL;"))
            conn.execute(text("ALTER TABLE users ALTER COLUMN security_question DROP NOT NULL;"))
            conn.execute(text("ALTER TABLE users ALTER COLUMN security_answer DROP NOT NULL;"))
            print("Updated existing columns to allow null values for OAuth users.")
        except Exception as e:
            print("Could not alter constraints:", e)
        
        conn.commit()

    print("PostgreSQL Migration complete.")

if __name__ == '__main__':
    migrate_pg()
