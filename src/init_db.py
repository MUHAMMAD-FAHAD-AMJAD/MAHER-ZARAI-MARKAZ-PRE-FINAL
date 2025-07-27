import os
import sqlite3
import datetime
import bcrypt


def init_db():
    db_path = os.path.join("data", "maher_zarai.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create tables
    cur.executescript(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        username TEXT UNIQUE,
        email TEXT,
        password_hash TEXT,
        role TEXT,
        created_at TEXT
    );
    
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        category TEXT,
        description TEXT,
        purchase_price REAL,
        selling_price REAL,
        stock_quantity INTEGER,
        min_stock_level INTEGER,
        supplier_id INTEGER,
        date_added DATE,
        FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
    );
    
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        address TEXT,
        balance REAL DEFAULT 0.0,
        created_at TEXT
    );
    
    CREATE TABLE IF NOT EXISTS suppliers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        contact_person TEXT,
        phone TEXT,
        email TEXT,
        address TEXT,
        created_at TEXT
    );
    
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        user_id INTEGER,
        sale_date TEXT,
        subtotal REAL,
        discount REAL,
        tax REAL,
        total REAL,
        payment_method TEXT,
        amount_paid REAL,
        udhaar_amount REAL,
        status TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    
    CREATE TABLE IF NOT EXISTS sale_items (
        id INTEGER PRIMARY KEY,
        sale_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        unit_price REAL,
        total_price REAL,
        FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(id)
    );
    
    CREATE TABLE IF NOT EXISTS udhaar_payments (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        amount REAL,
        payment_date TEXT,
        recorded_by INTEGER,
        notes TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(id),
        FOREIGN KEY (recorded_by) REFERENCES users(id)
    );
    
    CREATE TABLE IF NOT EXISTS user_activity (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        action TEXT,
        description TEXT,
        timestamp TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    );
    """
    )

    # Add default admin user if not exists
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    admin_exists = cur.execute(
        "SELECT id FROM users WHERE username = 'admin'"
    ).fetchone()

    if not admin_exists:
        admin_pass = bcrypt.hashpw("admin".encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )
        cur.execute(
            "INSERT INTO users (name, username, password_hash, role, created_at) VALUES (?, ?, ?, ?, ?)",
            ("Administrator", "admin", admin_pass, "Admin", current_time),
        )

    # Add default walk-in customer if not exists
    default_customer = cur.execute("SELECT id FROM customers WHERE id = 1").fetchone()
    if not default_customer:
        cur.execute(
            "INSERT INTO customers (id, name, created_at) VALUES (?, ?, ?)",
            (1, "Walk-in Customer", current_time),
        )

    # Add default supplier if not exists
    default_supplier = cur.execute("SELECT id FROM suppliers WHERE id = 1").fetchone()
    if not default_supplier:
        cur.execute(
            "INSERT INTO suppliers (id, name, contact_person, created_at) VALUES (?, ?, ?, ?)",
            (1, "Default Supplier", "Default Contact", current_time),
        )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
