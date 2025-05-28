import sqlite3
import time

conn = sqlite3.connect("notifications.db", check_same_thread=False)

cursor = conn.cursor()
'''
cursor.execute("""
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    message TEXT NOT NULL,
    read INTEGER DEFAULT 0,
    timestamp INTEGER NOT NULL
)
""")
conn.commit()
'''

def add_notification(user_id: str, message: str):
    timestamp = int(time.time())
    cursor.execute(
        "INSERT INTO notifications (user_id, message, read, timestamp) VALUES (?, ?, 0, ?)",
        (user_id, message, timestamp)
    )
    conn.commit()

def get_unread_notifications(user_id: str):
    cursor.execute(
        "SELECT id, message, timestamp FROM notifications WHERE user_id = ? AND read = 0 ORDER BY timestamp ASC",
        (user_id,)
    )
    return cursor.fetchall()

def get_recent_notifications(user_id: str, limit: int = 50):
    cursor.execute(
        "SELECT id, message, read, timestamp FROM notifications WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
        (user_id, limit)
    )
    return cursor.fetchall()

def mark_notifications_read(user_id: str):
    cursor.execute(
        "UPDATE notifications SET read = 1 WHERE user_id = ? AND read = 0",
        (user_id,)
    )
    conn.commit()
