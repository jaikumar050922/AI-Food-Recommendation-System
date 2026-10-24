import os
import sqlite3
from datetime import date, timedelta
from typing import Optional, Dict, Any, List, Tuple
from core.config import settings
from core.security import hash_password

def get_db_path() -> str:
    """
    Returns appropriate SQLite path:
    Uses /tmp in serverless/Vercel environments if no external DB is configured,
    or local data/nutriai.db in local development.
    """
    if os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
        return "/tmp/nutriai.db"
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "nutriai.db")


def get_db_connection():
    """
    Returns database connection with row factory enabled.
    Supports SQLite locally and /tmp on Vercel.
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    """Initializes tables for users, user_profiles, and progress tracking."""
    conn = get_db_connection()
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
    profile_data: Dict[str, Any]
) -> Tuple[bool, str, Optional[int]]:
    """Registers a new user and biometric profile."""
    email_clean = email.strip().lower()
    name_clean = name.strip()

    if not email_clean or "@" not in email_clean or "." not in email_clean:
        return False, "Please provide a valid email address.", None

    if len(password) < 6:
        return False, "Password must be at least 6 characters long.", None

    if not name_clean:
        return False, "Please enter your full name.", None

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM users WHERE email = ?;", (email_clean,))
        if cursor.fetchone():
            conn.close()
            return False, "An account with this email already exists. Please log in.", None

        pwd_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?);",
            (name_clean, email_clean, pwd_hash)
        )
        user_id = cursor.lastrowid

        allergies = profile_data.get("allergies", [])
        allergies_str = ",".join(allergies) if isinstance(allergies, list) else str(allergies or "")

        restrictions = profile_data.get("dietary_restrictions", profile_data.get("doctor_restrictions", []))
        restrictions_str = ",".join(restrictions) if isinstance(restrictions, list) else str(restrictions or "")

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
            float(profile_data.get("height_cm", profile_data.get("height", 172.0))),
            float(profile_data.get("weight_kg", profile_data.get("weight", 70.0))),
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

        # Initial starting progress entry
        today_str = date.today().isoformat()
        cursor.execute("""
        INSERT INTO progress (user_id, date, weight, calories, protein, carbs, fat, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            user_id,
            today_str,
            float(profile_data.get("weight_kg", profile_data.get("weight", 70.0))),
            0.0,
            0.0,
            0.0,
            0.0,
            "Initial starting weight recorded upon registration."
        ))

        conn.commit()
        conn.close()
        return True, "Account created successfully!", user_id

    except sqlite3.IntegrityError:
        conn.close()
        return False, "An account with this email already exists.", None
    except Exception as e:
        conn.close()
        return False, f"Registration error: {str(e)}", None


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Retrieve user credentials and identity by email."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?;", (email.strip().lower(),))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve basic user record by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, created_at FROM users WHERE id = ?;", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def get_user_profile(user_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve combined user profile and preferences."""
    conn = get_db_connection()
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

    allergies_list = [a.strip() for a in (row["allergies"] or "").split(",") if a.strip()]
    restrictions_list = [r.strip() for r in (row["dietary_restrictions"] or "").split(",") if r.strip()]

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
        "dietary_restrictions": restrictions_list,
        "doctor_custom_notes": row["doctor_custom_notes"] or ""
    }


def update_user_profile(user_id: int, profile_data: Dict[str, Any]) -> bool:
    """Updates user biometrics and preferences."""
    conn = get_db_connection()
    cursor = conn.cursor()

    allergies = profile_data.get("allergies", [])
    allergies_str = ",".join(allergies) if isinstance(allergies, list) else str(allergies or "")

    restrictions = profile_data.get("dietary_restrictions", profile_data.get("doctor_restrictions", []))
    restrictions_str = ",".join(restrictions) if isinstance(restrictions, list) else str(restrictions or "")

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

        if "name" in profile_data and profile_data["name"].strip():
            cursor.execute("UPDATE users SET name = ? WHERE id = ?;", (profile_data["name"].strip(), user_id))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating profile: {e}")
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
    notes: str = ""
) -> bool:
    """Logs daily progress tracking record."""
    conn = get_db_connection()
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

        if weight is not None and weight > 0:
            cursor.execute("UPDATE user_profiles SET weight = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?;", (weight, user_id))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding progress: {e}")
        conn.close()
        return False


def get_user_progress(user_id: int) -> List[Dict[str, Any]]:
    """Returns chronological list of historical progress entries."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, user_id, date, weight, calories, protein, carbs, fat, notes, created_at
    FROM progress
    WHERE user_id = ?
    ORDER BY date ASC, id ASC;
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def seed_demo_user():
    """Seeds the demo user account (demo@nutriai.com / Demo@1234) with 7 days of realistic history."""
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = 'demo@nutriai.com';")
    existing = cursor.fetchone()
    conn.close()

    if existing:
        return existing["id"]

    demo_profile = {
        "age": 28,
        "gender": "Male",
        "height_cm": 175.0,
        "weight_kg": 76.5,
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
        profile_data=demo_profile
    )

    if user_id:
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
                notes=note
            )

    return user_id
