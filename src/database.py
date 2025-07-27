# src/database.py

import os
import sqlite3
import datetime
import bcrypt
import logging
import shutil

# Configure logging to a file in a 'data' directory
log_dir = "data"
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, "app.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file_path), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


class Database:
    """
    Database handler for the MAHER ZARAI MARKAZ application using SQLite.
    This class manages all database interactions in a safe, transactional manner.
    """

    def __init__(self, db_path=None):
        """Initialize the database path."""
        if db_path is None:
            db_path = os.path.join("data", "maher_zarai.db")

        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.connection = None
        self._connect()
        self.initialize_db()

    def _connect(self):
        """Establish a database connection."""
        try:
            if self.connection is None or not self.connection:
                self.connection = sqlite3.connect(self.db_path, timeout=10)
                self.connection.row_factory = sqlite3.Row
                self.connection.execute("PRAGMA foreign_keys = ON")
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise

    def __enter__(self):
        """Enter the context manager, establishing a connection."""
        self._connect()
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager, committing or rolling back."""
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
                logger.error(f"Transaction rolled back due to error: {exc_val}")
            # Don't close the connection here, it will be reused

    def execute_query(self, query, params=None, fetch=None):
        """Execute a SQL query. Fetch 'one', 'all', or None."""
        if not self.connection:
            self._connect()

        try:
            if not self.connection:
                self._connect()

            cursor = self.connection.cursor()
            cursor.execute(query, params or ())

            result = None
            if fetch == "one":
                row = cursor.fetchone()
                result = dict(row) if row else None
            elif fetch == "all":
                rows = cursor.fetchall()
                result = [dict(row) for row in rows] if rows else []
            elif query.strip().upper().startswith("INSERT"):
                result = cursor.lastrowid
            else:
                result = True

            if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
                self.connection.commit()

            return result
        except sqlite3.Error as e:
            logger.error(f"Query failed: {e}\nQuery: {query}\nParams: {params}")
            if self.connection and query.strip().upper().startswith(
                ("INSERT", "UPDATE", "DELETE")
            ):
                self.connection.rollback()
            return [] if fetch == "all" else None

    def initialize_db(self):
        """Create all necessary tables and seed default data if they don't exist."""
        try:
            if not self.connection:
                self._connect()
            with self as cursor:
                # Core Tables
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, username TEXT UNIQUE, email TEXT, password_hash TEXT, role TEXT, created_at TEXT)"
                )
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, description TEXT, purchase_price REAL, selling_price REAL, stock_quantity INTEGER, min_stock_level INTEGER, supplier_id INTEGER, date_added DATE, FOREIGN KEY (supplier_id) REFERENCES suppliers(id))"
                )
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, address TEXT, balance REAL DEFAULT 0.0, created_at TEXT)"
                )
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS suppliers (id INTEGER PRIMARY KEY, name TEXT, contact_person TEXT, phone TEXT, email TEXT, address TEXT, created_at TEXT)"
                )
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY, customer_id INTEGER, user_id INTEGER, sale_date TEXT, subtotal REAL, discount REAL, tax REAL, total REAL, payment_method TEXT, amount_paid REAL, udhaar_amount REAL, status TEXT, FOREIGN KEY (customer_id) REFERENCES customers(id), FOREIGN KEY (user_id) REFERENCES users(id))"
                )
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS sale_items (id INTEGER PRIMARY KEY, sale_id INTEGER, product_id INTEGER, quantity INTEGER, unit_price REAL, total_price REAL, FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE, FOREIGN KEY (product_id) REFERENCES products(id))"
                )
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS udhaar_payments (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL, payment_date TEXT, recorded_by INTEGER, notes TEXT, FOREIGN KEY (customer_id) REFERENCES customers(id), FOREIGN KEY (recorded_by) REFERENCES users(id))"
                )
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS user_activity (id INTEGER PRIMARY KEY, user_id INTEGER, action TEXT, description TEXT, timestamp TEXT, FOREIGN KEY (user_id) REFERENCES users(id))"
                )
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)"
                )

                # Seed Default Data
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if (
                    self.execute_query(
                        "SELECT id FROM users WHERE username = 'admin'", fetch="one"
                    )
                    is None
                ):
                    admin_pass = bcrypt.hashpw(
                        "admin".encode("utf-8"), bcrypt.gensalt()
                    ).decode("utf-8")
                    self.execute_query(
                        "INSERT INTO users (name, username, password_hash, role, created_at) VALUES (?, ?, ?, ?, ?)",
                        ("Administrator", "admin", admin_pass, "Admin", current_time),
                    )
                if (
                    self.execute_query(
                        "SELECT id FROM customers WHERE id = 1", fetch="one"
                    )
                    is None
                ):
                    self.execute_query(
                        "INSERT INTO customers (id, name, created_at) VALUES (?, ?, ?)",
                        (1, "Walk-in Customer", current_time),
                    )
                default_settings = {
                    "shop_name": "MAHER ZARAI MARKAZ",
                    "theme": "light_green",
                }
                for key, value in default_settings.items():
                    self.execute_query(
                        "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)",
                        (key, value),
                    )

            logger.info("Database initialized successfully.")
            return True
        except sqlite3.Error as e:
            logger.error(f"Database initialization failed: {e}")
            return False

    # --- User Management ---
    def verify_user(self, username, password):
        user = self.execute_query(
            "SELECT * FROM users WHERE username = ?", (username,), fetch="one"
        )
        if user and bcrypt.checkpw(
            password.encode("utf-8"), user["password_hash"].encode("utf-8")
        ):
            self.log_activity(user["id"], "Login", f"User '{username}' logged in.")
            return user
        return None

    def get_all_users(self):
        return self.execute_query("SELECT * FROM users", fetch="all")

    def add_user(self, name, username, password, role):
        hashed_pass = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )
        return self.execute_query(
            "INSERT INTO users (name, username, password_hash, role, created_at) VALUES (?, ?, ?, ?, ?)",
            (
                name,
                username,
                hashed_pass,
                role,
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )

    def update_user(self, user_id, name, username, role):
        return self.execute_query(
            "UPDATE users SET name = ?, username = ?, role = ? WHERE id = ?",
            (name, username, role, user_id),
        )

    def delete_user(self, user_id):
        return self.execute_query("DELETE FROM users WHERE id = ?", (user_id,))

    def update_password(self, user_id, new_password):
        hashed_pass = bcrypt.hashpw(
            new_password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        return self.execute_query(
            "UPDATE users SET password_hash = ? WHERE id = ?", (hashed_pass, user_id)
        )

    # --- Product Management ---
    def add_product(self, data):
        return self.execute_query(
            "INSERT INTO products (name, category, purchase_price, selling_price, stock_quantity, min_stock_level, supplier_id, date_added) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                data["name"],
                data["category"],
                data["purchase_price"],
                data["selling_price"],
                data["stock_quantity"],
                data["min_stock_level"],
                data.get("supplier_id"),
                data.get("date_added", datetime.datetime.now().strftime("%Y-%m-%d")),
            ),
        )

    def get_all_products(self):
        try:
            products = self.execute_query(
                "SELECT p.*, s.name as supplier_name FROM products p LEFT JOIN suppliers s ON p.supplier_id = s.id ORDER BY p.name",
                fetch="all",
            )
            if products is None:
                logger.warning("No products found in the database.")
                return []
            return products
        except sqlite3.Error as e:
            logger.error(f"Error getting products: {e}")
            return []

    def update_product(self, product_id, data):
        return self.execute_query(
            "UPDATE products SET name=?, category=?, purchase_price=?, selling_price=?, stock_quantity=?, min_stock_level=?, supplier_id=? WHERE id=?",
            (
                data["name"],
                data["category"],
                data["purchase_price"],
                data["selling_price"],
                data["stock_quantity"],
                data["min_stock_level"],
                data.get("supplier_id"),
                product_id,
            ),
        )

    def delete_product(self, product_id):
        return self.execute_query("DELETE FROM products WHERE id=?", (product_id,))

    def get_product_categories(self):
        return self.execute_query(
            "SELECT DISTINCT category FROM products ORDER BY category", fetch="all"
        )

    def get_product_by_id(self, product_id):
        return self.execute_query(
            "SELECT * FROM products WHERE id = ?", (product_id,), fetch="one"
        )

    # --- Customer Management ---
    def add_customer(self, name, phone, address):
        return self.execute_query(
            "INSERT INTO customers (name, phone, address, created_at) VALUES (?, ?, ?, ?)",
            (
                name,
                phone,
                address,
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )

    def get_all_customers(self):
        return self.execute_query("SELECT * FROM customers ORDER BY name", fetch="all")

    def update_customer(self, customer_id, name, phone, address):
        return self.execute_query(
            "UPDATE customers SET name=?, phone=?, address=? WHERE id=?",
            (name, phone, address, customer_id),
        )

    def delete_customer(self, customer_id):
        return self.execute_query("DELETE FROM customers WHERE id=?", (customer_id,))

    # --- Supplier Management ---
    def add_supplier(self, name, contact, phone, email, address):
        return self.execute_query(
            "INSERT INTO suppliers (name, contact_person, phone, email, address, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (
                name,
                contact,
                phone,
                email,
                address,
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )

    def get_all_suppliers(self):
        return self.execute_query("SELECT * FROM suppliers ORDER BY name", fetch="all")

    def update_supplier(self, supplier_id, name, contact, phone, email, address):
        return self.execute_query(
            "UPDATE suppliers SET name=?, contact_person=?, phone=?, email=?, address=? WHERE id=?",
            (name, contact, phone, email, address, supplier_id),
        )

    def delete_supplier(self, supplier_id):
        return self.execute_query("DELETE FROM suppliers WHERE id=?", (supplier_id,))

    # --- Sales & Transactions ---
    def create_sale(self, sale_data):
        try:
            with self as cursor:
                cursor.execute(
                    "INSERT INTO sales (customer_id, user_id, sale_date, subtotal, discount, tax, total, payment_method, amount_paid, udhaar_amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        sale_data["customer_id"],
                        sale_data["user_id"],
                        sale_data["sale_date"],
                        sale_data["subtotal"],
                        sale_data["discount"],
                        sale_data["tax"],
                        sale_data["total"],
                        sale_data["payment_method"],
                        sale_data.get("amount_paid", 0),
                        sale_data.get("udhaar_amount", 0),
                    ),
                )
                sale_id = cursor.lastrowid
                for item in sale_data["items"]:
                    cursor.execute(
                        "INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, total_price) VALUES (?, ?, ?, ?, ?)",
                        (
                            sale_id,
                            item["product_id"],
                            item["quantity"],
                            item["price"],
                            item["total"],
                        ),
                    )
                    cursor.execute(
                        "UPDATE products SET stock_quantity = stock_quantity - ? WHERE id = ?",
                        (item["quantity"], item["product_id"]),
                    )
                if sale_data.get("udhaar_amount", 0) > 0:
                    cursor.execute(
                        "UPDATE customers SET balance = balance + ? WHERE id = ?",
                        (sale_data["udhaar_amount"], sale_data["customer_id"]),
                    )
                self.log_activity(
                    sale_data["user_id"],
                    "Create Sale",
                    f"Sale ID {sale_id}, Total: {sale_data['total']:.2f}",
                )
            return sale_id
        except sqlite3.Error as e:
            logger.error(f"Failed to create sale: {e}")
            return None

    def get_sale_details(self, sale_id):
        sale = self.execute_query(
            "SELECT s.*, c.name as customer_name, u.username as cashier FROM sales s JOIN customers c ON s.customer_id=c.id JOIN users u ON s.user_id=u.id WHERE s.id=?",
            (sale_id,),
            fetch="one",
        )
        items = self.execute_query(
            "SELECT si.*, p.name as product_name FROM sale_items si JOIN products p ON si.product_id=p.id WHERE si.sale_id=?",
            (sale_id,),
            fetch="all",
        )
        return {"sale": sale, "items": items}

    # --- Udhaar Management ---
    def add_udhaar_payment(self, customer_id, amount, recorded_by, notes):
        try:
            with self as cursor:
                cursor.execute(
                    "INSERT INTO udhaar_payments (customer_id, amount, payment_date, recorded_by, notes) VALUES (?, ?, ?, ?, ?)",
                    (
                        customer_id,
                        amount,
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        recorded_by,
                        notes,
                    ),
                )
                cursor.execute(
                    "UPDATE customers SET balance = balance - ? WHERE id = ?",
                    (amount, customer_id),
                )
            self.log_activity(
                recorded_by,
                "Udhaar Payment",
                f"Received {amount} from customer ID {customer_id}",
            )
            return True
        except sqlite3.Error as e:
            logger.error(f"Failed to add udhaar payment: {e}")
            return False

    # --- Reporting & Stats ---
    def get_all_products(self):
        """Get all products with supplier information."""
        try:
            products = self.execute_query(
                """
                SELECT 
                    p.*,
                    s.name as supplier_name
                FROM products p 
                LEFT JOIN suppliers s ON p.supplier_id = s.id 
                ORDER BY p.name
                """,
                fetch="all",
            )
            if products is None:
                logger.warning("No products found or error occurred")
                return []

            # Ensure all numeric fields are properly typed
            for p in products:
                try:
                    p["stock_quantity"] = (
                        int(p["stock_quantity"])
                        if p["stock_quantity"] is not None
                        else 0
                    )
                    p["min_stock_level"] = (
                        int(p["min_stock_level"])
                        if p["min_stock_level"] is not None
                        else 0
                    )
                    p["purchase_price"] = (
                        float(p["purchase_price"])
                        if p["purchase_price"] is not None
                        else 0.0
                    )
                    p["selling_price"] = (
                        float(p["selling_price"])
                        if p["selling_price"] is not None
                        else 0.0
                    )
                except (ValueError, TypeError) as e:
                    logger.error(f"Error converting product values: {e}")
                    continue

            return products
        except Exception as e:
            logger.error(f"Error in get_all_products: {e}")
            return []

    def get_sales(self, start_date=None, end_date=None):
        """Get sales data for a date range."""
        try:
            query = """
                SELECT 
                    s.*,
                    c.name as customer_name,
                    u.username as cashier_name
                FROM sales s
                LEFT JOIN customers c ON s.customer_id = c.id
                LEFT JOIN users u ON s.user_id = u.id
                WHERE 1=1
            """
            params = []

            if start_date:
                query += " AND DATE(s.sale_date) >= DATE(?)"
                params.append(start_date)
            if end_date:
                query += " AND DATE(s.sale_date) <= DATE(?)"
                params.append(end_date)

            query += " ORDER BY s.sale_date DESC"

            sales = self.execute_query(query, tuple(params), fetch="all")

            if sales is None:
                logger.warning(
                    f"No sales found for date range: {start_date} to {end_date}"
                )
                return []

            # Process the sales data to ensure proper types
            for sale in sales:
                try:
                    sale["subtotal"] = (
                        float(sale["subtotal"]) if sale["subtotal"] is not None else 0.0
                    )
                    sale["total"] = (
                        float(sale["total"]) if sale["total"] is not None else 0.0
                    )
                    sale["discount"] = (
                        float(sale["discount"]) if sale["discount"] is not None else 0.0
                    )
                    sale["tax"] = float(sale["tax"]) if sale["tax"] is not None else 0.0
                    sale["amount_paid"] = (
                        float(sale["amount_paid"])
                        if sale["amount_paid"] is not None
                        else 0.0
                    )
                    sale["udhaar_amount"] = (
                        float(sale["udhaar_amount"])
                        if sale["udhaar_amount"] is not None
                        else 0.0
                    )
                except (ValueError, TypeError) as e:
                    logger.error(f"Error converting sale values: {e}")
                    continue

            return sales
        except Exception as e:
            logger.error(f"Error getting sales data: {e}")
            return []

    def get_top_selling_products(self, start_date=None, end_date=None, limit=10):
        """Get top selling products for a date range."""
        try:
            query = """
                SELECT 
                    p.id,
                    p.name,
                    p.category,
                    COUNT(DISTINCT s.id) as num_sales,
                    SUM(si.quantity) as total_quantity,
                    SUM(si.total_price) as total_revenue,
                    AVG(si.unit_price) as avg_price
                FROM products p
                JOIN sale_items si ON p.id = si.product_id
                JOIN sales s ON si.sale_id = s.id
                WHERE 1=1
            """
            params = []

            if start_date:
                query += " AND DATE(s.sale_date) >= DATE(?)"
                params.append(start_date)
            if end_date:
                query += " AND DATE(s.sale_date) <= DATE(?)"
                params.append(end_date)

            query += """
                GROUP BY p.id
                ORDER BY total_quantity DESC
                LIMIT ?
            """
            params.append(limit)

            products = self.execute_query(query, tuple(params), fetch="all")

            if products is None:
                logger.warning("No products found in sales data")
                return []

            # Process the data to ensure proper types
            for product in products:
                try:
                    product["num_sales"] = (
                        int(product["num_sales"])
                        if product["num_sales"] is not None
                        else 0
                    )
                    product["total_quantity"] = (
                        int(product["total_quantity"])
                        if product["total_quantity"] is not None
                        else 0
                    )
                    product["total_revenue"] = (
                        float(product["total_revenue"])
                        if product["total_revenue"] is not None
                        else 0.0
                    )
                    product["avg_price"] = (
                        float(product["avg_price"])
                        if product["avg_price"] is not None
                        else 0.0
                    )
                except (ValueError, TypeError) as e:
                    logger.error(
                        f"Error converting product values for {product.get('name', 'Unknown')}: {e}"
                    )
                    continue

            return products
        except Exception as e:
            logger.error(f"Error getting top selling products: {e}")
            return []

    def get_monthly_sales_summary(self, year, month):
        """Get monthly sales summary."""
        try:
            query = """
                SELECT 
                    strftime('%Y-%m-%d', sale_date) as date,
                    COUNT(*) as num_sales,
                    SUM(total) as total_sales,
                    SUM(subtotal) as subtotal,
                    SUM(tax) as total_tax,
                    SUM(discount) as total_discount,
                    SUM(udhaar_amount) as total_udhaar
                FROM sales
                WHERE strftime('%Y', sale_date) = ? AND strftime('%m', sale_date) = ?
                GROUP BY strftime('%Y-%m-%d', sale_date)
                ORDER BY date DESC
            """

            month_str = str(month).zfill(2)  # Ensure month is 2 digits
            summary = self.execute_query(query, (str(year), month_str), fetch="all")

            if summary is None:
                logger.warning(f"No sales found for {year}-{month}")
                return []

            # Ensure numeric values are properly typed
            for day in summary:
                try:
                    day["num_sales"] = (
                        int(day["num_sales"]) if day["num_sales"] is not None else 0
                    )
                    day["total_sales"] = (
                        float(day["total_sales"])
                        if day["total_sales"] is not None
                        else 0.0
                    )
                    day["subtotal"] = (
                        float(day["subtotal"]) if day["subtotal"] is not None else 0.0
                    )
                    day["total_tax"] = (
                        float(day["total_tax"]) if day["total_tax"] is not None else 0.0
                    )
                    day["total_discount"] = (
                        float(day["total_discount"])
                        if day["total_discount"] is not None
                        else 0.0
                    )
                    day["total_udhaar"] = (
                        float(day["total_udhaar"])
                        if day["total_udhaar"] is not None
                        else 0.0
                    )
                except (ValueError, TypeError) as e:
                    logger.error(
                        f"Error converting sales values for {day['date']}: {e}"
                    )
                    continue

            return summary
        except Exception as e:
            logger.error(f"Error getting monthly sales summary: {e}")
            return []

    def get_daily_sales_summary(self, date):
        """Get daily sales summary for a specific date."""
        try:
            sales = self.execute_query(
                """
                SELECT 
                    s.*,
                    c.name as customer_name,
                    u.username as cashier_name
                FROM sales s
                LEFT JOIN customers c ON s.customer_id = c.id
                LEFT JOIN users u ON s.user_id = u.id
                WHERE DATE(s.sale_date) = DATE(?)
                ORDER BY s.sale_date DESC
                """,
                (date,),
                fetch="all",
            )

            if sales is None:
                logger.warning(f"No sales found for date: {date}")
                return []

            # Process the sales data to ensure proper types
            for sale in sales:
                try:
                    sale["subtotal"] = (
                        float(sale["subtotal"]) if sale["subtotal"] is not None else 0.0
                    )
                    sale["total"] = (
                        float(sale["total"]) if sale["total"] is not None else 0.0
                    )
                    sale["discount"] = (
                        float(sale["discount"]) if sale["discount"] is not None else 0.0
                    )
                    sale["tax"] = float(sale["tax"]) if sale["tax"] is not None else 0.0
                    sale["amount_paid"] = (
                        float(sale["amount_paid"])
                        if sale["amount_paid"] is not None
                        else 0.0
                    )
                    sale["udhaar_amount"] = (
                        float(sale["udhaar_amount"])
                        if sale["udhaar_amount"] is not None
                        else 0.0
                    )
                except (ValueError, TypeError) as e:
                    logger.error(f"Error converting sale values: {e}")
                    continue

            return sales
        except Exception as e:
            logger.error(f"Error getting daily sales summary: {e}")
            return []

    def get_dashboard_stats(self):
        today = datetime.date.today().strftime("%Y-%m-%d")
        stats = {}
        stats["today_sales"] = (
            self.execute_query(
                f"SELECT SUM(total) as total FROM sales WHERE sale_date LIKE '{today}%'",
                fetch="one",
            )["total"]
            or 0
        )
        stats["total_customers"] = (
            self.execute_query(
                "SELECT COUNT(id) as count FROM customers WHERE id != 1", fetch="one"
            )["count"]
            or 0
        )
        stats["low_stock_items"] = (
            self.execute_query(
                "SELECT COUNT(id) as count FROM products WHERE stock_quantity <= min_stock_level",
                fetch="one",
            )["count"]
            or 0
        )
        stats["total_udhaar"] = (
            self.execute_query(
                "SELECT SUM(balance) as total FROM customers", fetch="one"
            )["total"]
            or 0
        )
        return stats

    # --- Activity Log ---
    def log_activity(self, user_id, action, description=""):
        return self.execute_query(
            "INSERT INTO user_activity (user_id, action, description, timestamp) VALUES (?, ?, ?, ?)",
            (
                user_id,
                action,
                description,
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )

    # --- Settings ---
    def get_setting(self, key, default=None):
        result = self.execute_query(
            "SELECT value FROM settings WHERE key = ?", (key,), fetch="one"
        )
        return result["value"] if result else default

    def update_setting(self, key, value):
        self.log_activity(
            0, "Setting Change", f"Setting '{key}' changed."
        )  # User ID 0 for system
        return self.execute_query(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value)
        )

    # --- Backup & Restore ---
    def create_backup(self, backup_dir="data/backups"):
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"backup_{timestamp}.db")
        try:
            shutil.copy2(self.db_path, backup_path)
            logger.info(f"Database backup created: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return None

    def restore_from_backup(self, backup_path):
        if not os.path.exists(backup_path):
            logger.error(f"Backup file not found: {backup_path}")
            return False
        try:
            shutil.copy2(backup_path, self.db_path)
            logger.info(f"Database restored from: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to restore backup: {e}")
            return False
