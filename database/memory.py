import sqlite3 as sq
import os
import sys
import json
from datetime import datetime #عشان نجيب الوقت الدقيق
from pathlib import Path #مكتبه عشان نضيف باث ملف الاعداد عشان نعرف نقراه من هنا 

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config import DATABASE_PATH

def init_db():#هنا بنشيك اذا كان في ملف قاعدة بيانات ولا لا لو ماكانش بننشئ واحد جديد وبعدين بننشئ جدول للجلسات وجدول للرسائل
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sq.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    title TEXT default "محادثه جديده"
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

def create_session(title="محادثة جديدة"):#هنا بننشئ جلسة جديدة في قاعدة البيانات وبنرجع ال id بتاعها عشان نستخدمه في تخزين الرسائل الخاصة بيها
    conn = sq.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sessions (title, start_time)
        VALUES (?, ?)
    """, (title, datetime.now().isoformat()))

    session_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return session_id


def get_all_sessions():#هنا بنجيب كل الجلسات اللي موجودة في قاعدة البيانات وبنرتبها حسب تاريخ الانشاء من الاحدث للاقدم وبنرجعها في شكل قائمة من القواميس
    conn = sq.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, start_time
        FROM sessions
        ORDER BY start_time DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {"id": row[0],
        "title": row[1],
        "start_time": row[2]}
        for row in rows
    ]

def save_message(session_id, role, content, sources=None):#هنا بنخزن رسالة جديدة في قاعدة البيانات مع ربطها بالجلسة المناسبة عن طريق ال session_id وبنخزن الدور والمحتوى والمصادر والتاريخ والوقت اللي اتخزنت فيه الرسالة
    conn = sq.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO messages (session_id, role, content, sources, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (session_id, role, content, sources, datetime.now().isoformat()))

    conn.commit()
    conn.close()

def save_file(session_id, file_name, file_path, extracted_text=None):#هنا بنخزن ملف جديد في قاعدة البيانات مع ربطه بالجلسة المناسبة عن طريق ال session_id وبنخزن اسم الملف ومساره والنص المستخرج منه (لو موجود) والتاريخ والوقت اللي اتخزن فيه الملف
    # بنحفظ الملف في جدول files
    conn = sq.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO files (session_id, file_name, file_path, extracted_text, uploaded_at)
        VALUES (?, ?, ?, ?, ?)
    """, (session_id, file_name, file_path, extracted_text, datetime.now().isoformat()))

    file_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # بعد ما حفظنا الملف، بنحفظ في messages إشارة إنه موجود في المحادثة
    # content بيكون JSON فيه الـ file_id والاسم عشان نعرف نرجعه
    import json
    file_reference = json.dumps({"file_id": file_id, "name": file_name}, ensure_ascii=False)
    save_message(session_id, role="file", content=file_reference)

    return file_id
    

def get_session_messages(session_id):#هنا بنجيب كل الرسائل اللي مرتبطة بجلسة معينة عن طريق ال session_id وبنرتبها حسب تاريخ الانشاء من الاقدم للاحدث وبنرجعها في شكل قائمة من القواميس
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
        {
            "role": row[0],
            "content": row[1],
            "sources": row[2],
            "created_at": row[3]
        }
        for row in rows
    ]

def get_session_files(session_id):
    # بنجيب كل الملفات المرتبطة بجلسة معينة
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
        {
            "id":             row[0],
            "file_name":      row[1],
            "file_path":      row[2],
            "extracted_text": row[3],
            "uploaded_at":    row[4]
        }
        for row in rows
    ]

init_db()
