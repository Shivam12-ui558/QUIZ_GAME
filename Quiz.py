import sqlite3 as db
import random

conn = db.connect("quiz.db")

def login(conn):
    username = input("Username: ")
    print("Username entered:", username)
    password = input("Password: ")

    cur = conn.cursor()
    cur.execute("SELECT role, status FROM login WHERE username=? AND password=?", (username, password))
    result = cur.fetchone()

    if result:
        role, status = result
        if status.lower() == "active":
            print(f"Welcome {username}! Role: {role}")
            return username
        else:
            print("Account is not active.")
            return None
    else:
        print("Invalid credentials.")
        return None

def quizGame(conn, username):
    limit = int(input("Enter the number of questions: "))

    cur = conn.cursor()
    cur.execute("SELECT * FROM questions")
    all_questions = cur.fetchall()

    if len(all_questions) == 0:
        print("No questions available.")
        return

    if limit > len(all_questions):
        print(f"Only {len(all_questions)} questions are available. Limiting to that.")
        limit = len(all_questions)

    random.shuffle(all_questions)
    questions = all_questions[:limit]

    score = 0
    for i, q in enumerate(questions, 1):
        print(f"\nQ{i}: {q[1]}")
        print(f"A: {q[2]}\nB: {q[3]}\nC: {q[4]}\nD: {q[5]}")
        answer = input("Your answer (A/B/C/D): ").strip().upper()
        if answer == q[6].upper():
            score += 1

    scoreper = (score / limit) * 100
    print(f"\n{username}, your score is {score} out of {limit} ({scoreper:.2f}%)")

    cur.execute('INSERT INTO leaderboard (name, score, "limit", scoreper) VALUES (?, ?, ?, ?)',
                (username, score, limit, scoreper))
    conn.commit()
    print("Score saved to leaderboard.")

def main():
    user = login(conn)
    if user:
        quizGame(conn, user)
    conn.close()

if __name__ == "__main__":
    main()
