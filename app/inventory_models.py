import logging
import sqlite3

from flask_login import current_user

from app.db import get_db_connection

USER_INVENTORY_QUERY = """
        SELECT inventory_id 
        FROM user_inventory 
        WHERE user_id = ?;
        """


class Inventory:
    def get_item(self):
        products_query = """
        SELECT product_name, price, quantity, last_updated 
        FROM store_inventory 
        WHERE inventory_id = ?;
        """

        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                result = cur.execute(
                    USER_INVENTORY_QUERY, (current_user.user_id,)
                ).fetchone()

                if result is None:
                    logging.error("No inventory found for the current user.")
                    return []

                inventory_id = result["inventory_id"]
                products = cur.execute(products_query, (inventory_id,)).fetchall()

                return products
        except sqlite3.DatabaseError as e:
            logging.error(f"Unexpected error while fetching items: {e}")
            return []

    def add_item(self, product_name, price, quantity) -> bool:
        inventory_insert_query = """
                INSERT INTO store_inventory 
                (inventory_id, product_name, price, quantity)
                VALUES (?, ?, ?, ?)
                """

        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                result = cur.execute(
                    USER_INVENTORY_QUERY, (current_user.user_id,)
                ).fetchone()

                if result is None:
                    logging.error("No inventory found for the current user.")
                    return False

                inventory_id = result["inventory_id"]
                cur.execute(
                    inventory_insert_query,
                    (inventory_id, product_name, price, quantity),
                )
                conn.commit()

                return True
        except sqlite3.IntegrityError as e:
            logging.error(f"Integrity error: {e}")
            return False
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return False

    def remove_item(self):
        pass

    def edit_item(self):
        pass


class Analytics:
    pass
    # TODO
    # Analytics (Computation bullshit)
