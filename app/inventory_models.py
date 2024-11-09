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
    # def get_all_items(self):
    #     products_query = """
    #     SELECT product_id, product_name, price, quantity, last_updated
    #     FROM products
    #     WHERE inventory_id = ?;
    #     """
    #
    #     try:
    #         with get_db_connection() as conn:
    #             cur = conn.cursor()
    #             result = cur.execute(
    #                 USER_INVENTORY_QUERY, (current_user.user_id,)
    #             ).fetchone()
    #
    #             if result is None:
    #                 logging.error("No inventory found for the current user.")
    #                 return []
    #
    #             inventory_id = result["inventory_id"]
    #             products = cur.execute(products_query, (inventory_id,)).fetchall()
    #
    #             return products
    #     except sqlite3.DatabaseError as e:
    #         logging.error(f"Unexpected error while fetching items: {e}")
    #         return []

    def get_item(self, product_id):
        products_query = """
        SELECT product_id, product_name, price, quantity, last_updated 
        FROM products
        WHERE inventory_id = ? AND product_id = ?;
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
                product = cur.execute(
                    products_query,
                    (
                        inventory_id,
                        product_id,
                    ),
                ).fetchone()

                return product
        except sqlite3.DatabaseError as e:
            logging.error(f"Unexpected error while fetching an item: {e}")
            return []

    def add_item(
        self,
        product_name: str | None = None,
        price: float | None = None,
        quantity: int | None = None,
        supplier_name: str | None = None,
        date: str | None = None,
    ) -> bool:
        product_insert_query = """
            INSERT INTO products
            (inventory_id, product_name, price, quantity, last_updated)
            VALUES (?, ?, ?, ?, ?)
            RETURNING product_id
        """
        supplier_insert_query = """
            INSERT INTO suppliers
            (product_id, supplier_name)
            VALUES (?, ?)
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
                    product_insert_query,
                    (inventory_id, product_name, price, quantity, date),
                )
                product_id = cur.lastrowid
                cur.execute(supplier_insert_query, (product_id, supplier_name))

                conn.commit()
                return True

        except sqlite3.IntegrityError as e:
            logging.error(f"Integrity error: {e}")
            return False

    def edit_item(
        self,
        product_id: int | None = None,
        product_name: str | None = None,
        price: float | None = None,
        quantity: int | None = None,
        supplier_name: str | None = None,
        date: str | None = None,
    ) -> bool:
        update_product_query = """
            UPDATE products 
            SET product_name = ?, price = ?, quantity = ?, last_updated = ?
            WHERE product_id = ? AND inventory_id = ?
        """
        update_supplier_query = """
            UPDATE suppliers 
            SET supplier_name = ?
            WHERE product_id = ?
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
                    update_product_query,
                    (
                        product_name,
                        price,
                        quantity,
                        date,
                        product_id,
                        inventory_id,
                    ),
                )
                cur.execute(update_supplier_query, (supplier_name, product_id))
                conn.commit()

                return True
        except sqlite3.DatabaseError as e:
            logging.error(f"Error editing item: {str(e)}")
            return False

    def remove_item(self, product_id: int | None = None):
        remove_query = """
            DELETE FROM products 
            WHERE product_id = ? AND inventory_id = ?
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
                    remove_query,
                    (
                        product_id,
                        inventory_id,
                    ),
                )
                conn.commit()
                return True
        except sqlite3.DatabaseError as e:
            logging.error(f"Error deleting item: {str(e)}")
            return False

    def get_total_items(self):
        query = """
            SELECT COUNT(*) 
            FROM products
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
                    return 0

                inventory_id = result["inventory_id"]
                cur.execute(query, (inventory_id,))
                total_items = cur.fetchone()[0]

            return total_items
        except sqlite3.DatabaseError as e:
            logging.error(f"Unexpected error while fetching total items: {e}")
            return 0

    def get_all_paginated_items(self, offset: int, limit: int):
        products_query = """
            SELECT product.product_id, product.product_name, product.price, 
                   product.quantity, product.last_updated, supplier.supplier_name
            FROM products product
            LEFT JOIN suppliers supplier ON product.product_id = supplier.product_id
            WHERE product.inventory_id = ?
            ORDER BY product.product_name
            LIMIT ? OFFSET ?
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
                cur.execute(products_query, (inventory_id, limit, offset))
                products = cur.fetchall()

                return products
        except sqlite3.DatabaseError as e:
            logging.error(f"Unexpected error while fetching items: {e}")
            return []


class Analytics:
    pass
    # TODO
    # Analytics (Computation bullshit)
