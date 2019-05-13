import sqlite3
import os

CREATE_TABLE_QUERY = (
        'CREATE TABLE IF NOT EXIST Users'
        '(login text, password text)'
        )

DATABASE_NAME = "users.db"

DATABASE_PATH = os.path.join(
    os.path.expanduser('~'),
    'cat_fight',
    DATABASE_NAME
)

def check_db():
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

    connection.commit()
    cursor.close()

