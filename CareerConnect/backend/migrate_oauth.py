import sqlite3

def migrate():
    conn = sqlite3.connect('careerconnect.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN oauth_provider VARCHAR;")
        print("Added oauth_provider column.")
    except sqlite3.OperationalError as e:
        print("oauth_provider column might already exist:", e)

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN oauth_id VARCHAR;")
        print("Added oauth_id column.")
    except sqlite3.OperationalError as e:
        print("oauth_id column might already exist:", e)

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN profile_picture VARCHAR;")
        print("Added profile_picture column.")
    except sqlite3.OperationalError as e:
        print("profile_picture column might already exist:", e)

    # Note: SQLite doesn't support adding UNIQUE constraint via ALTER TABLE ADD COLUMN easily,
    # but we can rely on application-level checks or recreate the table if strictly needed.
    # For now, this is sufficient.
    
    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == '__main__':
    migrate()
