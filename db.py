import sqlite3
import os
import hashlib
import uuid
import random

from datetime import datetime
from user_statistics import UserStatistics


CREATE_USERS_TABLE_QUERY = (
    'CREATE TABLE IF NOT EXISTS  Users'
    '(id integer primary key autoincrement, user_name text, password text, token text, registration_date timestamp, status text, enemy_id int, battle_id int)'
)

CREATE_BATTLES_TABLE_QUERY = (
    'CREATE TABLE IF NOT EXISTS Battles  '
    '(id integer primary key autoincrement, current_turn_user_id int, winner_id int, loser_id int)'
)

CREATE_POINTS_TABLE_QUERY = (
    'CREATE TABLE IF NOT EXISTS Poinst  '
    '(battle_id int, x int, y int, crossed_points int)'
)

DATABASE_PATH = "cat_fight.db"

DATABASE_PATH = os.path.join(
    os.path.expanduser('~'),
    'wg_forge_study',
    'cat_fight',
    DATABASE_PATH
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

    cursor.execute(CREATE_USERS_TABLE_QUERY)
    cursor.execute(CREATE_BATTLES_TABLE_QUERY)
    cursor.execute(CREATE_POINTS_TABLE_QUERY)

    
    cursor.close()
    connection.commit()
    connection.close()
    

def get_user_id_by_name(user_name):
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


def get_user_id_by_token(token):
    connection = sqlite3.connect(DATABASE_PATH,  detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()

    cursor.execute('SELECT id FROM Users WHERE token = ?', (token, ))
    row = cursor.fetchone()
    if row:
        user_id = row[0]
    else:
        user_id = None
    cursor.close()
    connection.close()

    return user_id


def delete_token(user_id):
    connection = sqlite3.connect(DATABASE_PATH,  detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    status = 'logged out'

    cursor.execute('UPDATE Users SET status = ?, token = NULL WHERE id = ?', (status, user_id))
    
    cursor.close()
    connection.commit()
    connection.close()


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


def get_user_stats(user_id):
    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cursor = connection.cursor()

    cursor.execute('SELECT user_name, registration_date, status FROM Users WHERE id = ?', (user_id, ))   
    row = cursor.fetchone()
    user_statistics = UserStatistics(row[0], row[1], row[2])
    cursor.close()
    connection.close()
    
    return user_statistics

def find_enemy(user_id):
    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cursor = connection.cursor()

    cursor.execute('SELECT id, user_name FROM Users WHERE id <> ? and status = "logged in"', (user_id, ))
    rows = cursor.fetchall()
    if not rows:
        return None
    enemy_row = random.choice(rows)
    enemy_id = enemy_row[0]
    enemy_name = enemy_row[1]

    cursor.execute('UPDATE Users SET enemy_id = ?, status = "fighting" WHERE id = ?', (enemy_id, user_id))
    cursor.execute('UPDATE Users SET enemy_id = ?, status = "fighting" WHERE id = ?', (user_id, enemy_id))
    # cursor.execute('')
    # random.choice([user_id, enemy_id])
    cursor.close()
    connection.commit()
    connection.close()
    
    return enemy_name


def get_user_enemy(user_id):
    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cursor = connection.cursor()

    cursor.execute('SELECT enemy_id FROM Users WHERE id = ?', (user_id,))
    enemy_id = cursor.fetchone()[0]
    if not enemy_id:
        return None
    
    cursor.execute('SELECT user_name FROM Users WHERE id = ?', (enemy_id, ))
    enemy_name = cursor.fetchone()[0]
    
    cursor.close()
    connection.close()

    return enemy_name 
