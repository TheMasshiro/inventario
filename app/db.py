import os
import sqlite3


def get_db_connection():
    conn = sqlite3.connect("./app/database.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    if os.path.exists("./app/database.db"):
        return

    with get_db_connection() as conn:
        with open("./app/schema.sql") as file:
            conn.executescript(file.read())
            conn.commit()
