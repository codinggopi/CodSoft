import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("Error: DATABASE_URL not found in .env")
    exit(1)

engine = create_engine(DATABASE_URL)

sql_statements = [
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;",
    "UPDATE users SET is_active = TRUE WHERE is_active IS NULL;",
    "ALTER TABLE companies ADD COLUMN IF NOT EXISTS status VARCHAR DEFAULT 'Active';",
    "UPDATE companies SET status = 'Active' WHERE status IS NULL;",
    "ALTER TABLE users ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP;",
    "ALTER TABLE jobs ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP;",
    "ALTER TABLE applications ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP;"
]

with engine.begin() as conn:
    for stmt in sql_statements:
        try:
            conn.execute(text(stmt))
            print(f"Executed: {stmt}")
        except Exception as e:
            print(f"Skipped (or failed) executing: {stmt}\nReason: {e}")

print("\nDatabase schema synchronization complete!")
