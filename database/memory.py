import sqlite3 as sq
import os
import sys
from pathlib import Path #مكتبه عشان نضيف باث ملف الاعدار عشان نعرف نقراه من هنا 

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config import DATABASE_PATH
def init_db():#هنا بنشيك اذا كان في ملف قاعدة بيانات ولا لا لو ماكانش بننشئ واحد جديد وبعدين بننشئ جدول للجلسات وجدول للرسائل
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sq.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
                CREATE TABLE sessions (
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
    conn.commit()
    conn.close()
init_db()