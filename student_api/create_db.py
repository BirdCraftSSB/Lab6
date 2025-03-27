import sqlite3

def create_database():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            dob DATE NOT NULL,
            amount_due REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_database()
