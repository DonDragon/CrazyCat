import sqlite3

conn = sqlite3.connect("bonus.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    bonus_points INTEGER DEFAULT 0
)
""")
conn.commit()

def add_user(user_id, username):
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()

def get_balance(user_id):
    cursor.execute("SELECT bonus_points FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    return row[0] if row else 0

def add_bonus(user_id, points):
    cursor.execute("UPDATE users SET bonus_points = bonus_points + ? WHERE user_id = ?", (points, user_id))
    conn.commit()

def use_bonus(user_id, points):
    cursor.execute("UPDATE users SET bonus_points = bonus_points - ? WHERE user_id = ?", (points, user_id))
    conn.commit()
