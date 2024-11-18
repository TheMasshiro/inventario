import logging
import sqlite3

from flask_login import current_user

from app.db import get_db_connection

USER_INVENTORY_QUERY = """
        SELECT inventory_id 
        FROM user_inventory 
        WHERE user_id = ?;
        """


class Suppliers:
    def get_suppliers(self):
        suppliers_query = """
            SELECT *
            FROM suppliers
            WHERE inventory_id = ?
            ORDER BY company_name;
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

                cur.execute(suppliers_query, (inventory_id,))
                suppliers = cur.fetchall()

            return suppliers
        except sqlite3.DatabaseError as e:
            logging.error(f"Unexpected error while fetching suppliers: {e}")
            return None

    def search_supplier(self, q):
        supplier_query = """
        SELECT supplier_id,
                company_name,
                supplier_name,
                email,
                phone,
                status
        FROM suppliers
        WHERE inventory_id = ? 
        AND (company_name LIKE ? OR supplier_name LIKE ?)
        ORDER BY company_name;
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

                cur.execute(supplier_query, (inventory_id, search_term, search_term))
                suppliers = cur.fetchall()

                return suppliers or []
        except sqlite3.DatabaseError as e:
            logging.error(f"Unexpected error while fetching suppliers: {e}")
            return []

    def get_supplier_by_name(
        self, company_name: str | None = None, supplier_name: str | None = None
    ):
        supplier_query = """
        SELECT supplier_id,
                company_name,
                supplier_name,
                email,
                phone,
                status
        FROM suppliers
        WHERE company_name = ? AND supplier_name = ? AND inventory_id = ?
        """
        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                result = cur.execute(
                    USER_INVENTORY_QUERY, (current_user.user_id,)
                ).fetchone()

                if result is None:
                    logging.error("No supplier found for the current user.")
                    return None

                inventory_id = result["inventory_id"]

                supplier = cur.execute(
                    supplier_query, (company_name, supplier_name, inventory_id)
                ).fetchone()

                return supplier
        except sqlite3.DatabaseError as e:
            logging.error(f"Unexpected error while fetching item: {e}")
            return None

    def get_supplier_by_email(
        self, company_name: str | None = None, email: str | None = None
    ):
        supplier_query = """
        SELECT supplier_id,
                company_name,
                supplier_name,
                email,
                phone,
                status
        FROM suppliers
        WHERE company_name = ? AND email = ? AND inventory_id = ?
        """
        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                result = cur.execute(
                    USER_INVENTORY_QUERY, (current_user.user_id,)
                ).fetchone()

                if result is None:
                    logging.error("No supplier found for the current user.")
                    return None

                inventory_id = result["inventory_id"]

                supplier = cur.execute(
                    supplier_query, (company_name, email, inventory_id)
                ).fetchone()

                return supplier
        except sqlite3.DatabaseError as e:
            logging.error(f"Unexpected error while fetching item: {e}")
            return None

    def get_supplier_by_phone(
        self, company_name: str | None = None, phone: str | None = None
    ):
        supplier_query = """
        SELECT supplier_id,
                company_name,
                supplier_name,
                email,
                phone,
                status
        FROM suppliers
        WHERE company_name = ? AND phone = ? AND inventory_id = ?
        """
        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                result = cur.execute(
                    USER_INVENTORY_QUERY, (current_user.user_id,)
                ).fetchone()

                if result is None:
                    logging.error("No supplier found for the current user.")
                    return None

                inventory_id = result["inventory_id"]

                supplier = cur.execute(
                    supplier_query, (company_name, phone, inventory_id)
                ).fetchone()

                return supplier
        except sqlite3.DatabaseError as e:
            logging.error(f"Unexpected error while fetching item: {e}")
            return None

    def get_supplier(self, supplier_id: int | None = None):
        supplier_query = """
            SELECT supplier_id,
                    company_name,
                    supplier_name,
                    email,
                    phone,
                    status
            FROM suppliers
            WHERE supplier_id = ? AND inventory_id = ?
        """
        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                result = cur.execute(
                    USER_INVENTORY_QUERY, (current_user.user_id,)
                ).fetchone()

                if result is None:
                    logging.error("No supplier found for the current user.")
                    return None

                inventory_id = result["inventory_id"]

                supplier = cur.execute(
                    supplier_query, (supplier_id, inventory_id)
                ).fetchone()

                return supplier
        except sqlite3.DatabaseError as e:
            logging.error(f"Unexpected error while fetching item: {e}")
            return None

    def add_supplier(
        self,
        company_name: str | None = None,
        supplier_name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        status: str | None = None,
    ) -> bool:
        supplier_insert_query = """
            INSERT INTO suppliers
            (
                inventory_id, 
                company_name, 
                supplier_name, 
                email, 
                phone, 
                status
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """

        try:
            with get_db_connection() as conn:
                cur = conn.cursor()

                result = cur.execute(
                    USER_INVENTORY_QUERY, (current_user.user_id,)
                ).fetchone()

                if result is None:
                    logging.error("No supplier found for the current user.")
                    return False

                inventory_id = result["inventory_id"]

                cur.execute(
                    supplier_insert_query,
                    (
                        inventory_id,
                        company_name,
                        supplier_name,
                        email,
                        phone,
                        status,
                    ),
                )

                conn.commit()
                return True

        except sqlite3.IntegrityError as e:
            logging.error(f"Integrity error: {e}")
            return False

    def edit_supplier(
        self,
        supplier_id: int | None = None,
        company_name: str | None = None,
        supplier_name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        status: str | None = None,
    ) -> bool:
        update_product_query = """
            UPDATE suppliers
            SET company_name = ?, 
                supplier_name = ?, 
                email = ?, 
                phone = ?, 
                status = ?
            WHERE supplier_id = ? AND inventory_id = ?
        """
        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                result = cur.execute(
                    USER_INVENTORY_QUERY, (current_user.user_id,)
                ).fetchone()

                if result is None:
                    logging.error("No supplier found for the current user.")
                    return False

                inventory_id = result["inventory_id"]

                cur.execute(
                    update_product_query,
                    (
                        company_name,
                        supplier_name,
                        email,
                        phone,
                        status,
                        supplier_id,
                        inventory_id,
                    ),
                )
                conn.commit()

                return True
        except sqlite3.DatabaseError as e:
            logging.error(f"Error editing item: {str(e)}")
            return False

    def remove_supplier(self, supplier_id: int | None = None):
        remove_query = """
            DELETE FROM suppliers
            WHERE supplier_id = ? AND inventory_id = ?
        """
        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                result = cur.execute(
                    USER_INVENTORY_QUERY, (current_user.user_id,)
                ).fetchone()

                if result is None:
                    logging.error("No suppliers found for the current user.")
                    return False

                inventory_id = result["inventory_id"]

                cur.execute(
                    remove_query,
                    (
                        supplier_id,
                        inventory_id,
                    ),
                )
                conn.commit()
                return True
        except sqlite3.DatabaseError as e:
            logging.error(f"Error deleting item: {str(e)}")
            return False
