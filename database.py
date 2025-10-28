import sqlite3
import bcrypt

# ---------------- Database Setup ----------------
def init_db():
    conn = sqlite3.connect("pneumonia_app.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            result TEXT,
            timestamp DATETIME,
            FOREIGN KEY (email) REFERENCES users (email)
        )
    """
    )
    conn.commit()
    conn.close()

# ---------------- Password Helpers ----------------
def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def verify_password(stored_hash, provided_password):
    return bcrypt.checkpw(provided_password.encode("utf-8"), stored_hash)