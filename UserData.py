import sqlite3 as db

conn = db.connect("quiz.db")
cur = conn.cursor()

username = input("Enter new username: ")
password = input("Enter password: ")
role = input("Enter role (e.g., user/admin): ")
status = "active"

try:
    cur.execute("INSERT INTO login (username, password, role, status) VALUES (?, ?, ?, ?)",
                (username, password, role, status))
    conn.commit()
    print(f"User '{username}' created successfully.")
except Exception as e:
    print("Error:", e)

conn.close()
