import sqlite3
import os
import hashlib
import uuid

from datetime import datetime
from user_statistics import UserStatistics


CREATE_TABLE_QUERY = (
        'CREATE TABLE IF NOT EXISTS  Users'
        '(login text, password text, token text, registration_date date)'
        )

DATABASE_NAME = "users.db"

DATABASE_PATH = os.path.join(
    os.path.expanduser('~'),
    'wg_forge_study',
    'cat_fight',
    DATABASE_NAME
)

def init_db():
    if os.path.exists(DATABASE_PATH):
        print("Aborting initialization, db already exists")
        return

    print("No database found. Initializing new database.")

    database_dir = os.path.dirname(DATABASE_PATH)

    if not os.path.exists(database_dir):
        os.makedirs(database_dir)

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(CREATE_TABLE_QUERY)

    cursor.close()
    connection.commit()
    connection.close()
    

def user_exists(login):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Users WHERE login = ?', (login, ))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    return user is not None


def generate_token(login, password):
    hash_password = make_hash(password)

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    token = uuid.uuid4().hex

    cursor.execute('UPDATE Users SET token = ? WHERE login = ? and password = ?', (token, login, hash_password,))
    
    cursor.close()
    connection.commit()
    connection.close()

    return token


def make_hash(string):
    return hashlib.sha1(string.encode()).hexdigest()


def password_is_correct(login, password):
    hash_password = make_hash(password)
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute('SELECT login FROM Users WHERE login = ? and password = ?', (login, hash_password))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    return user is not None


def new_user(login, password):
    hash_password = make_hash(password)
    registration_date = datetime.now()
    

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute('INSERT INTO Users (login, password, registration_date) VALUES(?,?,?)', (login, hash_password, registration_date))
    
    cursor.close()
    connection.commit()
    connection.close()


def token_is_valid(token):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute('SELECT token FROM Users WHERE token = ?', (token, ))
    user_token = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    return user_token is not None

def get_user_stats(user_name):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT registration_date FROM Users WHERE login = ?", (user_name, ))   
    row = cursor.fetchone()
    user_statistics = UserStatistics(user_name, row[0])
    cursor.close()
    connection.close()
    return user_statistics
    

