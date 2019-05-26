import sqlite3
import os
import hashlib
import uuid

from datetime import datetime
from user_statistics import UserStatistics


CREATE_TABLE_QUERY = (
        'CREATE TABLE IF NOT EXISTS  Users'
        '(id integer primary key autoincrement, user_name text, password text, token text, registration_date timestamp, status text)'
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

    connection = sqlite3.connect(DATABASE_PATH,  detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()

    cursor.execute(CREATE_TABLE_QUERY)

    cursor.close()
    connection.commit()
    connection.close()
    

def get_user_id(user_name):
    connection = sqlite3.connect(DATABASE_PATH,  detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()

    cursor.execute('SELECT id FROM Users WHERE user_name = ?', (user_name, ))
    row = cursor.fetchone()
    if row:
        user_id = row[0]
    else:
        user_id = None
    cursor.close()
    connection.close()

    return user_id

def generate_token(user_id):

    connection = sqlite3.connect(DATABASE_PATH,  detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    token = uuid.uuid4().hex
    status = "logged in"

    cursor.execute('UPDATE Users SET token = ?, status = ? WHERE id = ?', (token, status, user_id))
    
    cursor.close()
    connection.commit()
    connection.close()

    return token


def make_hash(string):
    return hashlib.sha1(string.encode()).hexdigest()


def password_is_correct(user_name, password):
    hash_password = make_hash(password)
    connection = sqlite3.connect(DATABASE_PATH,  detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    
    cursor.execute('SELECT user_name FROM Users WHERE user_name = ? and password = ?', (user_name, hash_password))
    
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    return user is not None


def new_user(user_name, password):
    hash_password = make_hash(password)
    registration_date = datetime.now()
    

    connection = sqlite3.connect(DATABASE_PATH,  detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()

    cursor.execute('INSERT INTO Users (user_name, password, registration_date, status) VALUES(?,?,?, "logged out")', (user_name, hash_password, registration_date))
    
    cursor.close()
    connection.commit()
    connection.close()


def token_is_valid(token):
    connection = sqlite3.connect(DATABASE_PATH,  detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()

    cursor.execute('SELECT token FROM Users WHERE token = ?', (token, ))
    user_token = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    return user_token is not None

def get_user_stats(user_id):
    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cursor = connection.cursor()
    print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n", user_id, type(user_id), "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")

    cursor.execute("SELECT user_name, registration_date, status FROM Users WHERE id = ?", (user_id, ))   
    row = cursor.fetchone()
    print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n", row[1], type(row[1]), "\n!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
    user_statistics = UserStatistics(row[0], row[1], row[2])
    cursor.close()
    connection.close()
    return user_statistics
    

