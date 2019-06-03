import sqlite3
import os
import hashlib
import uuid
import random
import psycopg2

from datetime import datetime
from user_statistics import UserStatistics

from game_field import Point


CREATE_USERS_TABLE_QUERY = (
    'CREATE TABLE IF NOT EXISTS  Users'
    '(id integer primary key autoincrement, user_name text, password text, token text, registration_date timestamp, status text, enemy_id int, battle_id int)'
)

CREATE_BATTLES_TABLE_QUERY = (
    'CREATE TABLE IF NOT EXISTS Battles  '
    '(id integer primary key autoincrement, field_length int, field_height int, current_turn_user_id int, winner_id int, loser_id int)'
)

CREATE_POINTS_TABLE_QUERY = (
    'CREATE TABLE IF NOT EXISTS Points  '
    '(entity_id int, x int, y int)'
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


    current_turn_users_id = random.choice([user_id, enemy_id])

    field_length = 5
    field_height = 5
    
    cursor.execute('INSERT INTO Battles (current_turn_user_id, field_length, field_height) VALUES(, ?, ?)', (current_turn_users_id, field_length, field_height))
    battle_id = cursor.lastrowid
    cursor.execute('UPDATE Users SET enemy_id = ?, battle_id = ?, status = "fighting" WHERE id = ?', (enemy_id, battle_id, user_id))
    cursor.execute('UPDATE Users SET enemy_id = ?, battle_id = ?, status = "fighting" WHERE id = ?', (user_id, battle_id, enemy_id))
    cursor.execute('INSERT INTO Points(entity_id, x, y) VALUES(?, ?, ?)', (user_id, 0 , 0))
    cursor.execute('INSERT INTO Points(entity_id, x, y) VALUES(?, ?, ?)', (enemy_id, field_length , field_height))

    cursor.close()
    connection.commit()
    connection.close()
    
    return enemy_name


def get_current_turn_user_id(user_id):
    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cursor = connection.cursor()
    
    cursor.execute('SELECT current_turn_user_id FROM Battles WHERE id IN (SELECT battle_id FROM Users WHERE id = ?)',(user_id, ))
    
    row = cursor.fetchone()

    if not row:
        return None

    current_turn_user_id = row[0]

    cursor.close()
    connection.commit()
    connection.close()

    return current_turn_user_id


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


def make_action(user_id, action):
    battle_won = False
    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cursor = connection.cursor()

    cursor.execute('SELECT x, y FROM Points WHERE entity_id = ?', (user_id, ))
    point_row = cursor.fetchone()
    if not point_row:
        return None, battle_won
    user_point = Point(point_row[0], point_row[1])
    prev_user_point = Point(user_point.x, user_point.y)
    cursor.execute('SELECT field_length, field_height, id FROM Battles WHERE id IN (SELECT battle_id FROM Users WHERE id = ?)', (user_id, ))
    battle_row = cursor.fetchone()
    if not battle_row:
        return None, battle_won
    
    field_length = battle_row[0]
    field_height = battle_row[1]
    battle_id = battle_row[2]

    if action == 'up':
        if (user_point.y + 1) > field_height:
            return None, battle_won
        else:
            user_point.y += 1
    elif action == 'down':
        if (user_point.y - 1) < 0:
            return None, battle_won
        else:
            user_point.y -= 1
    elif action == 'left':
        if (user_point.x - 1) < 0:
            return None
        else:
            user_point.x -= 1
    elif action == 'right':
        if (user_point.x + 1) > field_length:
            return None, battle_won
        else:
            user_point.x += 1
    cursor.execute(
        'UPDATE Points SET x = ?, y = ? WHERE entity_id = ?',
        (user_point.x, user_point.y, user_id, )
    )
    cursor.execute(
        'INSERT INTO POINTS(entity_id, x, y) VALUES(?, ?, ?)',
        (battle_id, prev_user_point.x, prev_user_point.y)
    )
    cursor.execute('SELECT x, y FROM Points WHERE entity_id = ?', (battle_id, ))
    set_points_rows = cursor.fetchall()
    
    if not set_points_rows:
        return None, battle_won
    set_points = [
        Point(row[0], row[1])
        for row in set_points_rows
    ]

    cursor.execute('SELECT x, y FROM Points WHERE entity_id IN (SELECT enemy_id from Users where id = ?)', (user_id, ))
    enemy_row = cursor.fetchone()
    if not enemy_row:
        return None, battle_won
    enemy_point = Point(enemy_row[0], enemy_row[1])

    enemy_neighbour_points = [
        Point(enemy_point.x + 1, enemy_point.y),
        Point(enemy_point.x - 1, enemy_point.y),
        Point(enemy_point.x, enemy_point.y + 1),
        Point(enemy_point.x, enemy_point.y - 1),
    ]

    enemy_neighbour_points = [
        point
        for point in enemy_neighbour_points
        if point.x > 0 and point.y > 0 and point.x <= field_length and point.y <= field_height 
    ]

    all_neighbour_points_set = True

    for point in enemy_neighbour_points:
        for set_point in set_points:
            if set_point.x != point.x or set_point.y != point.y:
                all_neighbour_points_set = False
                break

    if all_neighbour_points_set:
        battle_won = True
        cursor.execute('UPDATE Users SET status = "logged in" WHERE id in (SELECT winner_id FROM Battles WHERE battle_id = ?)', (battle_id, ))
        cursor.execute('UPDATE Users SET status = "logged in" WHERE id in (SELECT loser_id FROM Battles WHERE battle_id = ?)', (battle_id, ))
        cursor.execute('DELETE FROM Points WHERE entity_id in (?, ?, (SELECT enemy_id from Users where id = ?))', (user_id, battle_id, user_id))

    cursor.close()
    connection.commit()
    connection.close()
    
    return user_point, battle_won