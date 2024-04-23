# model.py

import sqlite3
from datetime import datetime

DB_NAME = "DasBoard.db"

class Message:
    def __init__(self, id, name, email, mobile, date, message):
        self.id = id
        self.name = name
        self.email = email
        self.mobile = mobile
        self.date = date
        self.message = message

def create_table():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            mobile TEXT,
            date TEXT,
            message TEXT
        )
    ''')

    connection.commit()
    connection.close()

def insert_message(name, email, mobile, message):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO messages (name, email, mobile, date, message)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, email, mobile, date, message))

    connection.commit()
    connection.close()

def get_all_messages():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM messages')
    columns = [column[0] for column in cursor.description]
    messages = [Message(*row) for row in cursor.fetchall()]

    connection.close()
    return messages

def delete_message(message_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute('DELETE FROM messages WHERE id = ?', (message_id,))

    connection.commit()
    connection.close()
