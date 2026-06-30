import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        ) 
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,   
            news TEXT NOT NULL,
            result TEXT NOT NULL,
            confidence REAL NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database created successfully!")