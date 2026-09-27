"""
Database & Authentication Module for NutriAI
Uses SQLite with PBKDF2-HMAC-SHA256 password hashing.
Handles users, user profiles, and personal progress tracking.
"""

import os
import sqlite3
import hashlib
import hmac
from datetime import datetime, date, timedelta
from typing import Optional, Dict, Any, Tuple
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "nutriai.db")


def get_db_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Create a connection with row factory enabled."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def hash_password(password: str) -> str:
    """Generate a secure PBKDF2-HMAC-SHA256 hash with a random 16-byte salt."""
    salt = os.urandom(16).hex()
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    ).hex()
    return f"{salt}${pwd_hash}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify password against stored salt$hash string."""
    try:
        salt, expected_hash = stored_hash.split("$", 1)
        calc_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100000
        ).hex()
        return hmac.compare_digest(calc_hash, expected_hash)
    except Exception:
        return False


def init_db(db_path: str = DB_PATH):
    """Initialize database tables if they do not exist."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. User Profiles Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_profiles (
        user_id INTEGER PRIMARY KEY,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        height REAL NOT NULL,
        weight REAL NOT NULL,
        target_weight REAL,
        activity_level TEXT NOT NULL,
        food_preference TEXT NOT NULL,
        primary_goal TEXT NOT NULL,
        allergies TEXT DEFAULT '',
        custom_allergies TEXT DEFAULT '',
        foods_to_avoid TEXT DEFAULT '',
        dietary_restrictions TEXT DEFAULT '',
        doctor_custom_notes TEXT DEFAULT '',
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # 3. Progress Tracking Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        weight REAL,
        calories REAL,
        protein REAL,
        carbs REAL,
        fat REAL,
        notes TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()


def register_user(
    name: str,
    email: str,
    password: str,
    profile_data: Dict[str, Any],
    db_path: str = DB_PATH
) -> Tuple[bool, str, Optional[int]]:
    """
    Registers a new user and creates their biometric profile.
    Returns (success, message, user_id).
    """
    email_clean = email.strip().lower()
    name_clean = name.strip()

    if not email_clean or "@" not in email_clean or "." not in email_clean:
        return False, "Please provide a valid email address.", None

    if len(password) < 6:
        return False, "Password must be at least 6 characters long.", None

    if not name_clean:
        return False, "Please enter your full name.", None

    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    try:
        # Check duplicate email
        cursor.execute("SELECT id FROM users WHERE email = ?;", (email_clean,))
        if cursor.fetchone():
            conn.close()
            return False, "An account with this email already exists. Please log in.", None

        # Insert User
        pwd_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?);",
            (name_clean, email_clean, pwd_hash)
        )
        user_id = cursor.lastrowid

        # Insert User Profile
        allergies_str = ",".join(profile_data.get("allergies", [])) if isinstance(profile_data.get("allergies"), list) else str(profile_data.get("allergies", ""))
        restrictions_str = ",".join(profile_data.get("dietary_restrictions", [])) if isinstance(profile_data.get("dietary_restrictions"), list) else str(profile_data.get("dietary_restrictions", ""))

        cursor.execute("""
        INSERT INTO user_profiles (
            user_id, age, gender, height, weight, target_weight,
            activity_level, food_preference, primary_goal,
            allergies, custom_allergies, foods_to_avoid,
            dietary_restrictions, doctor_custom_notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            user_id,
            int(profile_data.get("age", 28)),
            str(profile_data.get("gender", "Male")),
            float(profile_data.get("height", 172.0)),
            float(profile_data.get("weight", 70.0)),
            float(profile_data.get("target_weight", profile_data.get("weight", 70.0))),
            str(profile_data.get("activity_level", "Moderately Active (moderate exercise 3-5 days/wk)")),
            str(profile_data.get("food_preference", "Vegetarian")),
            str(profile_data.get("primary_goal", "Weight Loss")),
            allergies_str,
            str(profile_data.get("custom_allergies", "")),
            str(profile_data.get("foods_to_avoid", "")),
            restrictions_str,
            str(profile_data.get("doctor_custom_notes", ""))
        ))

        # Add initial starting progress entry
        today_str = date.today().isoformat()
        cursor.execute("""
        INSERT INTO progress (user_id, date, weight, calories, protein, carbs, fat, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            user_id,
            today_str,
            float(profile_data.get("weight", 70.0)),
            0.0,
            0.0,
            0.0,
            0.0,
            "Initial starting weight recorded upon registration."
        ))

        conn.commit()
        conn.close()
        return True, "Account created successfully! You can now log in.", user_id

    except sqlite3.IntegrityError:
        conn.close()
        return False, "An account with this email already exists.", None
    except Exception as e:
        conn.close()
        return False, f"Registration error: {str(e)}", None


def authenticate_user(email: str, password: str, db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    """
    Validates user credentials.
    Returns user dictionary if authenticated, otherwise None.
    """
    email_clean = email.strip().lower()
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT u.id, u.name, u.email, u.password_hash, u.created_at
    FROM users u
    WHERE u.email = ?;
    """, (email_clean,))
    row = cursor.fetchone()
    conn.close()

    if row and verify_password(password, row["password_hash"]):
        return {
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "created_at": row["created_at"]
        }
    return None


def get_user_profile(user_id: int, db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    """Retrieve full user profile and preferences."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT u.name, u.email, p.*
    FROM users u
    JOIN user_profiles p ON u.id = p.user_id
    WHERE u.id = ?;
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    # Parse comma separated fields to lists
    allergies_list = [a.strip() for a in row["allergies"].split(",") if a.strip()]
    restrictions_list = [r.strip() for r in row["dietary_restrictions"].split(",") if r.strip()]

    return {
        "user_id": row["user_id"],
        "name": row["name"],
        "email": row["email"],
        "age": int(row["age"]),
        "gender": row["gender"],
        "height_cm": float(row["height"]),
        "weight_kg": float(row["weight"]),
        "target_weight": float(row["target_weight"]) if row["target_weight"] is not None else float(row["weight"]),
        "activity_level": row["activity_level"],
        "food_preference": row["food_preference"],
        "primary_goal": row["primary_goal"],
        "allergies": allergies_list,
        "custom_allergies": row["custom_allergies"] or "",
        "foods_to_avoid": row["foods_to_avoid"] or "",
        "doctor_restrictions": restrictions_list,
        "doctor_custom_notes": row["doctor_custom_notes"] or ""
    }


def update_user_profile(user_id: int, profile_data: Dict[str, Any], db_path: str = DB_PATH) -> bool:
    """Updates user biometrics and preferences."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    allergies_str = ",".join(profile_data.get("allergies", [])) if isinstance(profile_data.get("allergies"), list) else str(profile_data.get("allergies", ""))
    restrictions_str = ",".join(profile_data.get("dietary_restrictions", [])) if isinstance(profile_data.get("dietary_restrictions"), list) else str(profile_data.get("dietary_restrictions", ""))

    try:
        cursor.execute("""
        UPDATE user_profiles
        SET age = ?, gender = ?, height = ?, weight = ?, target_weight = ?,
            activity_level = ?, food_preference = ?, primary_goal = ?,
            allergies = ?, custom_allergies = ?, foods_to_avoid = ?,
            dietary_restrictions = ?, doctor_custom_notes = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?;
        """, (
            int(profile_data.get("age", 28)),
            str(profile_data.get("gender", "Male")),
            float(profile_data.get("height_cm", profile_data.get("height", 172.0))),
            float(profile_data.get("weight_kg", profile_data.get("weight", 70.0))),
            float(profile_data.get("target_weight", 70.0)),
            str(profile_data.get("activity_level", "Moderately Active (moderate exercise 3-5 days/wk)")),
            str(profile_data.get("food_preference", "Vegetarian")),
            str(profile_data.get("primary_goal", "Weight Loss")),
            allergies_str,
            str(profile_data.get("custom_allergies", "")),
            str(profile_data.get("foods_to_avoid", "")),
            restrictions_str,
            str(profile_data.get("doctor_custom_notes", "")),
            user_id
        ))

        # Also update name in users if provided
        if "name" in profile_data and profile_data["name"].strip():
            cursor.execute("UPDATE users SET name = ? WHERE id = ?;", (profile_data["name"].strip(), user_id))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Update error: {e}")
        conn.close()
        return False


def add_progress_entry(
    user_id: int,
    date_str: str,
    weight: Optional[float] = None,
    calories: Optional[float] = None,
    protein: Optional[float] = None,
    carbs: Optional[float] = None,
    fat: Optional[float] = None,
    notes: str = "",
    db_path: str = DB_PATH
) -> bool:
    """Adds a daily progress tracking entry for a user."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO progress (user_id, date, weight, calories, protein, carbs, fat, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            user_id,
            date_str,
            weight,
            calories or 0.0,
            protein or 0.0,
            carbs or 0.0,
            fat or 0.0,
            notes.strip()
        ))

        # If weight is provided, also sync current weight in user_profiles
        if weight is not None and weight > 0:
            cursor.execute("UPDATE user_profiles SET weight = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?;", (weight, user_id))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding progress: {e}")
        conn.close()
        return False


def get_user_progress(user_id: int, db_path: str = DB_PATH) -> pd.DataFrame:
    """Returns a pandas DataFrame of all historical progress for the given user."""
    conn = get_db_connection(db_path)
    query = """
    SELECT id, date, weight, calories, protein, carbs, fat, notes, created_at
    FROM progress
    WHERE user_id = ?
    ORDER BY date ASC, id ASC;
    """
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    return df


def seed_demo_user(db_path: str = DB_PATH):
    """
    Seeds a high-quality demo account (demo@nutriai.com / Demo@1234)
    with realistic profile and 7-day progress history for immediate presentation.
    """
    init_db(db_path)
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE email = 'demo@nutriai.com';")
    existing = cursor.fetchone()
    conn.close()

    if existing:
        return existing["id"]

    demo_profile = {
        "age": 28,
        "gender": "Male",
        "height": 175.0,
        "weight": 76.5,
        "target_weight": 70.0,
        "activity_level": "Moderately Active (moderate exercise 3-5 days/wk)",
        "food_preference": "Vegetarian",
        "primary_goal": "Weight Loss",
        "allergies": ["Dairy"],
        "custom_allergies": "",
        "foods_to_avoid": "mushroom, eggplant",
        "dietary_restrictions": ["Low Sodium / Hypertension Friendly"],
        "doctor_custom_notes": "Maintain daily sodium under 2000mg, prioritize plant protein."
    }

    success, msg, user_id = register_user(
        name="Alex Morgan",
        email="demo@nutriai.com",
        password="Demo@1234",
        profile_data=demo_profile,
        db_path=db_path
    )

    if user_id:
        # Seed 6 days of progress history leading up to today
        today = date.today()
        history = [
            (today - timedelta(days=6), 78.0, 1950, 140, 180, 55, "Started NutriAI meal plan"),
            (today - timedelta(days=5), 77.8, 1900, 145, 175, 52, "Adhered strictly to plan"),
            (today - timedelta(days=4), 77.4, 1880, 150, 160, 50, "Energy levels great"),
            (today - timedelta(days=3), 77.1, 1920, 148, 170, 54, "Gym workout completed"),
            (today - timedelta(days=2), 76.9, 1850, 152, 165, 48, "Met all macro targets"),
            (today - timedelta(days=1), 76.7, 1890, 149, 168, 51, "Rest day, good recovery"),
            (today, 76.5, 1870, 155, 160, 49, "Weighed in this morning")
        ]
        for day_date, w, cal, p, c, f, note in history:
            add_progress_entry(
                user_id=user_id,
                date_str=day_date.isoformat(),
                weight=w,
                calories=cal,
                protein=p,
                carbs=c,
                fat=f,
                notes=note,
                db_path=db_path
            )

    return user_id


# Initialize DB and seed demo user on import
init_db()
seed_demo_user()
