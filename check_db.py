import sqlite3
import os


CREATE_TABLE_QUERY = (
        'CREATE TABLE IF NOT EXISTS  Users'
        '(login text, password text)'
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

    cursor.execute('SELECT * FROM Users WHERE login = ?', (login,))
    users = cursor.fetchone()
    cursor.close()
    connection.close()

    return users is not None

def new_user(login, password):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute('INSERT INTO Users (login, password) VALUES(?,?)', (login, password))
    
    cursor.close()
    connection.commit()
    connection.close()



    

