import sqlite3
import json
from pathlib import Path

DB_PATH = "conversations.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            data TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_conversation(session_id, data: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO sessions (session_id, data)
        VALUES (?, ?)
    ''', (session_id, json.dumps(data)))
    conn.commit()
    conn.close()

def get_conversation(session_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT data FROM sessions WHERE session_id = ?', (session_id,))
    row = c.fetchone()
    conn.close()
    return json.loads(row[0]) if row else {}
