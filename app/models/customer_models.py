import logging
import sqlite3

from flask_login import current_user

from app.db import get_db_connection

USER_INVENTORY_QUERY = """
        SELECT inventory_id 
        FROM user_inventory 
        WHERE user_id = ?;
        """


class Analytics:
    def get_low_stock_products(self):
        query = """
            SELECT *
            FROM products
            WHERE inventory_id = ? AND stock <= 10
            ORDER BY stock;
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

                cur.execute(query, (inventory_id,))
                products = cur.fetchall()

                return products or []
        except sqlite3.DatabaseError as e:
            logging.error(f"Unexpected error while fetching low stock products: {e}")
            return []

    def get_best_selling_products(self):
        query = """
            SELECT 
                product.product_id,
                product.product_name,
                SUM(sale.sold) as total_sold,
                product.price,
                product.supplier_name
            FROM sales sale
            JOIN products product ON sale.product_id = product.product_id
            WHERE sale.inventory_id = ? AND sale.sold > 0
            GROUP BY product.product_id, product.product_name, product.price , product.supplier_name
            ORDER BY total_sold DESC;
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

                cur.execute(query, (inventory_id,))
                products = cur.fetchall()

                return products or []
        except sqlite3.DatabaseError as e:
            logging.error(f"Unexpected error while fetching best selling products: {e}")
            return []


class Customers:
    def get_customers(self):
        customers_query = """
            SELECT *
            FROM customers
            WHERE inventory_id = ?
            ORDER BY customer_name;
        """
        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                result = cur.execute(
                    USER_INVENTORY_QUERY, (current_user.user_id,)
                ).fetchone()

                if result is None:
                    logging.error("No inventory found for the current user.")
                    return

                inventory_id = result["inventory_id"]

                cur.execute(customers_query, (inventory_id,))
                customers = cur.fetchall()

            return customers
        except sqlite3.DatabaseError as e:
            logging.error(f"Unexpected error while fetching customers: {e}")
            return None

    def search_customer(self, q):
        search_query = """
        SELECT *
        FROM customers
        WHERE inventory_id = ? AND customer_name LIKE ?
        ORDER BY customer_name;
        """

        search_term = f"%{q}%"
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

                cur.execute(search_query, (inventory_id, search_term))
                customers = cur.fetchall()

                return customers or []
        except sqlite3.DatabaseError as e:
            logging.error(f"Unexpected error while fetching customers: {e}")
            return []

    def get_customer_by_name(self, customer_name):
        customer_query = """
            SELECT *
            FROM customers
            WHERE customer_name = ? AND inventory_id = ?;
        """
        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                result = cur.execute(
                    USER_INVENTORY_QUERY, (current_user.user_id,)
                ).fetchone()

                if result is None:
                    logging.error("No inventory found for the current user.")
                    return

                inventory_id = result["inventory_id"]

                cur.execute(customer_query, (customer_name, inventory_id))
                customer = cur.fetchone()

            return customer
        except sqlite3.DatabaseError as e:
            logging.error(f"Unexpected error while fetching customer: {e}")
            return None

    def get_customer(self, customer_id):
        customer_query = """
            SELECT *
            FROM customers
            WHERE customer_id = ? AND inventory_id = ?;
        """
        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                result = cur.execute(
                    USER_INVENTORY_QUERY, (current_user.user_id,)
                ).fetchone()

                if result is None:
                    logging.error("No inventory found for the current user.")
                    return

                inventory_id = result["inventory_id"]

                cur.execute(customer_query, (customer_id, inventory_id))
                customer = cur.fetchone()

            return customer
        except sqlite3.DatabaseError as e:
            logging.error(f"Unexpected error while fetching customer: {e}")
            return None

    def add_customer(self, customer_name):
        query = """
            INSERT INTO customers (customer_name, inventory_id) 
            VALUES (?, ?);
        """
        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                result = cur.execute(
                    USER_INVENTORY_QUERY, (current_user.user_id,)
                ).fetchone()

                if result is None:
                    logging.error("No inventory found for the current user.")
                    return

                inventory_id = result["inventory_id"]

                cur.execute(query, (customer_name, inventory_id))
                conn.commit()

                return True
        except sqlite3.DatabaseError as e:
            logging.error(f"Unexpected error while adding customer: {e}")
            return False

    def edit_customer(self, customer_id, customer_name):
        customer_query = """
            UPDATE customers
            SET customer_name = ?
            WHERE customer_id = ? AND inventory_id = ?;
        """
        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                result = cur.execute(
                    USER_INVENTORY_QUERY, (current_user.user_id,)
                ).fetchone()

                if result is None:
                    logging.error("No inventory found for the current user.")
                    return

                inventory_id = result["inventory_id"]

                cur.execute(customer_query, (customer_name, customer_id, inventory_id))
                conn.commit()

                return True
        except sqlite3.DatabaseError as e:
            logging.error(f"Unexpected error while editing customer: {e}")
            return False

    def remove_customer(self, customer_id):
        query = """
            DELETE FROM customers 
            WHERE customer_id = ?;
        """
        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                cur.execute(query, (customer_id,))
                conn.commit()

                return True
        except sqlite3.DatabaseError as e:
            logging.error(f"Unexpected error while deleting customer: {e}")
            return False
