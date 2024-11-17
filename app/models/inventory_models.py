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
    def get_supplier_companies(self):
        supplier_company_query = """
        SELECT company_name
        FROM suppliers
        WHERE inventory_id = ?
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
                companies = cur.execute(
                    supplier_company_query,
                    (inventory_id,),
                ).fetchall()

                return companies
        except sqlite3.DatabaseError as e:
            logging.error(f"Unexpected error while fetching an item: {e}")
            return []

    def get_item_by_name_and_supplier(self, product_name: str, supplier_name: str):
        products_query = """
        SELECT product_id, 
               product_name, 
               price, stock, 
               last_updated, 
               supplier_name
        FROM products
        WHERE inventory_id = ? AND product_name = ? AND supplier_name = ?;
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
                        product_name,
                        supplier_name,
                    ),
                ).fetchone()

                return product
        except sqlite3.DatabaseError as e:
            logging.error(f"Unexpected error while fetching an item: {e}")
            return []

    def get_item_by_name(
        self,
        product_name: str | None = None,
    ):
        products_query = """
        SELECT product_id, 
               product_name, 
               price, stock, 
               last_updated, 
               supplier_name
        FROM products
        WHERE inventory_id = ? AND product_name = ?;
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
                        product_name,
                    ),
                ).fetchone()

                return product
        except sqlite3.DatabaseError as e:
            logging.error(f"Unexpected error while fetching an item: {e}")
            return []

    def get_item(self, product_id: int | None = None):
        products_query = """
        SELECT product_id, 
               product_name, 
               price, stock, 
               last_updated, 
               supplier_name
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
        stock: int | None = None,
        date: str | None = None,
        company_name: str | None = None,
    ) -> bool:
        product_insert_query = """
            INSERT INTO products
            (
                supplier_id, 
                inventory_id, 
                product_name, 
                supplier_name, 
                price, 
                stock, 
                last_updated
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        supplier_id_query = """
            SELECT supplier_id 
            FROM suppliers 
            WHERE company_name = ?
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

                supplier_result = cur.execute(
                    supplier_id_query, (company_name,)
                ).fetchone()

                if supplier_result is None:
                    logging.error("No supplier found for the current user.")
                    return False

                supplier_id = supplier_result["supplier_id"]

                cur.execute(
                    product_insert_query,
                    (
                        supplier_id,
                        inventory_id,
                        product_name,
                        company_name,
                        price,
                        stock,
                        date,
                    ),
                )

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
        stock: int | None = None,
        date: str | None = None,
        company_name: str | None = None,
    ) -> bool:
        update_product_query = """
            UPDATE products 
            SET supplier_id = ?,
                product_name = ?,
                supplier_name = ?,
                price = ?,
                stock = ?,
                last_updated = ?
            WHERE product_id = ? AND inventory_id = ?
        """

        supplier_id_query = """
            SELECT supplier_id 
            FROM suppliers 
            WHERE company_name = ?
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

                supplier_result = cur.execute(
                    supplier_id_query, (company_name,)
                ).fetchone()

                if supplier_result is None:
                    logging.error("No supplier found for the current user.")
                    return False

                supplier_id = supplier_result["supplier_id"]

                cur.execute(
                    update_product_query,
                    (
                        supplier_id,
                        product_name,
                        company_name,
                        price,
                        stock,
                        date,
                        product_id,
                        inventory_id,
                    ),
                )
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
            SELECT DISTINCT product_id,
                            product_name,
                            price,
                            stock,
                            last_updated,
                            supplier_name
            FROM products
            WHERE inventory_id = ?
            ORDER BY product_name
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
