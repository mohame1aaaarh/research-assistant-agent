import sqlite3 as sq
import os
import sys
import json
from datetime import datetime
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config import DATABASE_PATH

def init_db():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sq.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            username   TEXT    NOT NULL UNIQUE,
            password   TEXT    NOT NULL,
            created_at TEXT    NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            title      TEXT    DEFAULT "محادثة جديدة",
            start_time TEXT    NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            role       TEXT    NOT NULL,
            content    TEXT    NOT NULL,
            sources    TEXT    DEFAULT NULL,
            created_at TEXT    NOT NULL,
            FOREIGN KEY (session_id) REFERENCES sessions(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id     INTEGER NOT NULL,
            file_name      TEXT    NOT NULL,
            file_path      TEXT    NOT NULL,
            extracted_text TEXT    DEFAULT NULL,
            uploaded_at    TEXT    NOT NULL,
            FOREIGN KEY (session_id) REFERENCES sessions(id)
        )
    ''')

    conn.commit()
    conn.close()

def create_session(user_id: int, title="محادثة جديدة"):
    conn = sq.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sessions (user_id, title, start_time)
        VALUES (?, ?, ?)
    """, (user_id, title, datetime.now().isoformat()))
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_id

def create_user(username: str, hashed_password: str) -> int:
    conn = sq.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (username, password, created_at)
        VALUES (?, ?, ?)
    """, (username, hashed_password, datetime.now().isoformat()))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id

def get_user(username: str) -> dict:
    conn = sq.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, username, password, created_at
        FROM users
        WHERE username = ?
    """, (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "username": row[1], "password": row[2], "created_at": row[3]}
    return None

def get_user_by_id(user_id: int) -> dict:
    # بتجيب بيانات مستخدم عن طريق الـ id
    conn = sq.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, username, password, created_at
        FROM users
        WHERE id = ?
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "username": row[1], "password": row[2], "created_at": row[3]}
    return None

def get_user_sessions(user_id: int) -> list:
    conn = sq.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, start_time
        FROM sessions
        WHERE user_id = ?
        ORDER BY start_time DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [
        {"id": row[0], "title": row[1], "start_time": row[2]}
        for row in rows
    ]

def save_message(session_id, role, content, sources=None):
    conn = sq.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messages (session_id, role, content, sources, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (session_id, role, content, sources, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def save_file(session_id, file_name, file_path, extracted_text=None):
    conn = sq.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO files (session_id, file_name, file_path, extracted_text, uploaded_at)
        VALUES (?, ?, ?, ?, ?)
    """, (session_id, file_name, file_path, extracted_text, datetime.now().isoformat()))
    file_id = cursor.lastrowid
    conn.commit()
    conn.close()
    file_reference = json.dumps({"file_id": file_id, "name": file_name}, ensure_ascii=False)
    save_message(session_id, role="file", content=file_reference)
    return file_id

def get_session_messages(session_id):
    conn = sq.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT role, content, sources, created_at
        FROM messages
        WHERE session_id = ?
        ORDER BY created_at ASC
    """, (session_id,))
    rows = cursor.fetchall()
    conn.close()
    return [
        {"role": row[0], "content": row[1], "sources": row[2], "created_at": row[3]}
        for row in rows
    ]

def get_session_files(session_id):
    conn = sq.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, file_name, file_path, extracted_text, uploaded_at
        FROM files
        WHERE session_id = ?
        ORDER BY uploaded_at ASC
    """, (session_id,))
    rows = cursor.fetchall()
    conn.close()
    return [
        {"id": row[0], "file_name": row[1], "file_path": row[2],
         "extracted_text": row[3], "uploaded_at": row[4]}
        for row in rows
    ]
def get_thread_author(session_id: int) -> str:
    conn = sq.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.username
        FROM sessions s
        JOIN users u ON s.user_id = u.id
        WHERE s.id = ?
    """, (session_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else ""
def update_session_title(session_id: int, title: str):
    conn = sq.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE sessions SET title = ? WHERE id = ?", (title, session_id))
    conn.commit()
    conn.close()
init_db()