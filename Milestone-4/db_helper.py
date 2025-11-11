# db_helper.py (UPDATED - New Admin Credentials)
# Enhanced Database Helper with Admin Features

import sqlite3
from datetime import datetime
import hashlib

DB_NAME = "smartland.db"

# -----------------------------
# UTILS
# -----------------------------
def get_db():
    return sqlite3.connect(DB_NAME)

# -----------------------------
# INIT DB
# -----------------------------
def init_db():
    conn = get_db()
    c = conn.cursor()

    # USERS TABLE (Enhanced with role and created_at)
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TEXT,
            last_login TEXT
        )
    """)

    # PREDICTIONS TABLE
    c.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            timestamp TEXT,
            degree TEXT,
            major TEXT,
            skill1 TEXT,
            skill2 TEXT,
            certification TEXT,
            experience_years INTEGER,
            project_count INTEGER,
            internship TEXT,
            experience_level TEXT,
            predicted_label TEXT,
            confidence FLOAT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # FEEDBACK TABLE
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            timestamp TEXT,
            rating INTEGER,
            comments TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # MODEL LOGS TABLE (for tracking retraining)
    c.execute("""
        CREATE TABLE IF NOT EXISTS model_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            admin_id INTEGER,
            action TEXT,
            model_name TEXT,
            accuracy REAL,
            details TEXT,
            FOREIGN KEY(admin_id) REFERENCES users(id)
        )
    """)

    # DATASET UPLOADS TABLE
    c.execute("""
        CREATE TABLE IF NOT EXISTS dataset_uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            admin_id INTEGER,
            filename TEXT,
            rows_count INTEGER,
            status TEXT,
            FOREIGN KEY(admin_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    
    # Create default admin user if not exists
    create_default_admin(conn)
    
    conn.close()

def create_default_admin(conn):
    """Create default admin user with new credentials"""
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username='giridhar'")
    if not c.fetchone():
        # Create new admin with updated credentials
        c.execute("""
            INSERT INTO users (username, email, password_hash, role, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, ('giridhar', 'giridhar@smartland.com', hash_password('Giridhar@25'), 'admin', 
              datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        print("✅ Admin user created:")
        print("   Username: giridhar")
        print("   Password: Giridhar@25")
    else:
        # Admin already exists, update password if needed
        c.execute("""
            UPDATE users SET password_hash=? WHERE username='giridhar'
        """, (hash_password('Giridhar@25'),))
        conn.commit()
        print("✅ Admin credentials updated:")
        print("   Username: giridhar")
        print("   Password: Giridhar@25")

# -----------------------------
# USER FUNCTIONS
# -----------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password):
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO users (username, email, password_hash, role, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (username, email, hash_password(password), 'user', 
              datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, password_hash, role FROM users WHERE username=?", (username,))
    user = c.fetchone()
    
    if user and user[1] == hash_password(password):
        # Update last login
        c.execute("UPDATE users SET last_login=? WHERE id=?", 
                 (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user[0]))
        conn.commit()
        conn.close()
        return {'user_id': user[0], 'role': user[2]}
    
    conn.close()
    return None

def get_user_info(user_id):
    """Get user information"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT username, email, role, created_at, last_login FROM users WHERE id=?", (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return {
            'username': user[0],
            'email': user[1],
            'role': user[2],
            'created_at': user[3],
            'last_login': user[4]
        }
    return None

def update_user_profile(user_id, email):
    """Update user profile"""
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("UPDATE users SET email=? WHERE id=?", (email, user_id))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def change_password(user_id, old_password, new_password):
    """Change user password"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE id=?", (user_id,))
    user = c.fetchone()
    
    if user and user[0] == hash_password(old_password):
        c.execute("UPDATE users SET password_hash=? WHERE id=?", 
                 (hash_password(new_password), user_id))
        conn.commit()
        conn.close()
        return True
    
    conn.close()
    return False

# -----------------------------
# PREDICTION FUNCTIONS
# -----------------------------
def insert_prediction(user_id, row):
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        INSERT INTO predictions (
            user_id, timestamp, degree, major, skill1, skill2, certification,
            experience_years, project_count, internship, experience_level, predicted_label, confidence
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        row.get("Degree"),
        row.get("Major"),
        row.get("Skill1"),
        row.get("Skill2"),
        row.get("Certification"),
        row.get("ExperienceYears"),
        row.get("ProjectCount"),
        row.get("Internship"),
        row.get("ExperienceLevel"),
        row.get("predicted_label"),
        row.get("confidence", 0)
    ))
    conn.commit()
    conn.close()

def fetch_history(user_id, limit=100):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM predictions WHERE user_id=? ORDER BY id DESC LIMIT ?", (user_id, limit))
    rows = c.fetchall()
    conn.close()
    return rows

def get_user_prediction_count(user_id):
    """Get total prediction count for a user"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM predictions WHERE user_id=?", (user_id,))
    count = c.fetchone()[0]
    conn.close()
    return count

# -----------------------------
# FEEDBACK FUNCTIONS
# -----------------------------
def insert_feedback(user_id, rating, comments):
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO feedback (user_id, timestamp, rating, comments) VALUES (?, ?, ?, ?)",
              (user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), rating, comments))
    conn.commit()
    conn.close()

def get_all_feedback(limit=100):
    """Admin: Get all feedback"""
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT f.id, u.username, f.timestamp, f.rating, f.comments
        FROM feedback f
        JOIN users u ON f.user_id = u.id
        ORDER BY f.id DESC LIMIT ?
    """, (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_average_rating():
    """Get average app rating"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT AVG(rating) FROM feedback")
    avg = c.fetchone()[0]
    conn.close()
    return avg if avg else 0

# -----------------------------
# ADMIN FUNCTIONS
# -----------------------------
def get_all_users():
    """Admin: Get all users"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, username, email, role, created_at, last_login FROM users ORDER BY id DESC")
    users = c.fetchall()
    conn.close()
    return users

def delete_user(user_id):
    """Admin: Delete a user"""
    conn = get_db()
    c = conn.cursor()
    try:
        # Delete related predictions and feedback
        c.execute("DELETE FROM predictions WHERE user_id=?", (user_id,))
        c.execute("DELETE FROM feedback WHERE user_id=?", (user_id,))
        c.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def update_user_role(user_id, new_role):
    """Admin: Update user role"""
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("UPDATE users SET role=? WHERE id=?", (new_role, user_id))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def get_all_predictions(limit=1000):
    """Admin: Get all predictions"""
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT p.id, u.username, p.timestamp, p.degree, p.major, 
               p.skill1, p.skill2, p.predicted_label
        FROM predictions p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.id DESC LIMIT ?
    """, (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def log_model_action(admin_id, action, model_name, accuracy=None, details=None):
    """Admin: Log model retraining or updates"""
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        INSERT INTO model_logs (timestamp, admin_id, action, model_name, accuracy, details)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), admin_id, action, 
          model_name, accuracy, details))
    conn.commit()
    conn.close()

def get_model_logs(limit=50):
    """Admin: Get model logs"""
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT ml.id, u.username, ml.timestamp, ml.action, ml.model_name, 
               ml.accuracy, ml.details
        FROM model_logs ml
        JOIN users u ON ml.admin_id = u.id
        ORDER BY ml.id DESC LIMIT ?
    """, (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def log_dataset_upload(admin_id, filename, rows_count, status):
    """Admin: Log dataset upload"""
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        INSERT INTO dataset_uploads (timestamp, admin_id, filename, rows_count, status)
        VALUES (?, ?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), admin_id, 
          filename, rows_count, status))
    conn.commit()
    conn.close()

def get_dataset_uploads(limit=50):
    """Admin: Get dataset upload history"""
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT d.id, u.username, d.timestamp, d.filename, d.rows_count, d.status
        FROM dataset_uploads d
        JOIN users u ON d.admin_id = u.id
        ORDER BY d.id DESC LIMIT ?
    """, (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

# -----------------------------
# STATISTICS FUNCTIONS
# -----------------------------
def get_dashboard_stats():
    """Get statistics for dashboard"""
    conn = get_db()
    c = conn.cursor()
    
    # Total users
    c.execute("SELECT COUNT(*) FROM users WHERE role='user'")
    total_users = c.fetchone()[0]
    
    # Total predictions
    c.execute("SELECT COUNT(*) FROM predictions")
    total_predictions = c.fetchone()[0]
    
    # Total feedback
    c.execute("SELECT COUNT(*) FROM feedback")
    total_feedback = c.fetchone()[0]
    
    # Average rating
    c.execute("SELECT AVG(rating) FROM feedback")
    avg_rating = c.fetchone()[0] or 0
    
    # Most predicted role
    c.execute("""
        SELECT predicted_label, COUNT(*) as count
        FROM predictions
        GROUP BY predicted_label
        ORDER BY count DESC
        LIMIT 1
    """)
    top_role = c.fetchone()
    
    conn.close()
    
    return {
        'total_users': total_users,
        'total_predictions': total_predictions,
        'total_feedback': total_feedback,
        'avg_rating': round(avg_rating, 2),
        'top_role': top_role[0] if top_role else 'N/A',
        'top_role_count': top_role[1] if top_role else 0
    }