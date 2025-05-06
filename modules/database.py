import os
import sqlite3

database = os.getenv('DATABASE')

def create_table():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            face TEXT NOT NULL,
            credential TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_user(face, credential):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (face, credential)
        VALUES (?, ?)
    ''', (face, credential))
    conn.commit()
    conn.close()

def get_user_by_credential(credential):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE credential = ?', (credential,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_all_users():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users