import logging
import os
import sqlite3
from datetime import datetime
from hashlib import md5

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import login


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


@login.user_loader
def load_user(user_id):
    user = User(user_id=user_id)
    logging.info(user)  # Debugging line
    return user.get_user("user_id")


class User(UserMixin):
    def __init__(
        self,
        username=None,
        password_hash=None,
        store_name=None,
        user_id=None,
        created=None,
    ) -> None:
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.store_name = store_name
        self.created = created

    def __repr__(self):
        return f"<User user_id={self.user_id} username={self.username}>"

    def get_id(self):
        """Returns the unique identifier of the user"""
        return str(self.user_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        email = f"{self.username}@email.com"
        digest = md5(email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

    def get_user(self, identifier_type="username"):
        """Get user data based on the initialized attributes.
        Args:
            identifier_type (str): The type of identifier used (default: "username").
        Returns:
            User: A User object if found, None otherwise.
        Raises:
            ValueError: If an invalid identifier_type is provided.
        """

        allowed_identifiers = ["username", "user_id", "email"]
        if identifier_type not in allowed_identifiers:
            raise ValueError(
                f"Invalid identifier_type. Must be one of {allowed_identifiers}"
            )

        identifier = getattr(self, identifier_type, None)
        if identifier is None:
            logging.error(f"{identifier_type} is not set in the User instance.")
            return None

        query = f"SELECT * FROM users WHERE {identifier_type} = ?"

        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                cur.execute(query, (identifier,))
                user_data = cur.fetchone()
                if user_data:
                    user = User(
                        user_id=user_data["user_id"],
                        username=user_data["username"],
                        password_hash=user_data["password_hash"],
                        store_name=user_data["store_name"]
                        if user_data["store_name"]
                        else None,
                        created=datetime.strptime(
                            user_data["created"], "%Y-%m-%d %H:%M:%S"
                        )
                        if user_data["created"]
                        else None,
                    )
                    return user
                return None

        except sqlite3.DatabaseError as e:
            logging.error(f"Database Error: {e}")
            return None

    def create_user(self) -> bool:
        """Create a new user.
        Returns:
            bool: `True` if the user was created successfully, `False` otherwise.
        Raise:
            UniqueViolation: Ensure the username/email is unique.
        """

        query = "INSERT INTO users (username, password_hash) VALUES (?, ?)"

        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    query,
                    (self.username, self.password_hash),
                )
                conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            logging.error(e)
            return False
        except Exception as e:
            logging.error(e)
            return False

    def update_user(self):
        # TODO: right now
        """
        Not Implemented yet
        """
        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                if self.store_name is None:
                    query = "UPDATE users SET password_hash = ? WHERE username = ?"
                    cur.execute(
                        query,
                        (self.password_hash, self.username),
                    )
                else:
                    query = "UPDATE users SET store_name = ? WHERE username = ?"
                    cur.execute(
                        query,
                        (self.store_name, self.username),
                    )
                conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            logging.error(e)
            return False
        except Exception as e:
            logging.error(e)
            return False

    def delete_user(self) -> bool:
        """Delete a user.
        Returns:
            bool: `True` if the user was deleted successfully, `False` otherwise.
        Raise:
            Sqlite3.Error: Ensure that the user is deleted.
        """
        query = "DELETE FROM users WHERE username = ?"

        if not self.username:
            return False

        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                cur.execute(query, (self.username))
                conn.commit()
                if cur.rowcount == 0:
                    return False
            return True

        except sqlite3.Error as e:
            logging.error(e)
            return False
