import sqlite3
import json
from pathlib import Path

DB_FILE = Path(__file__).parent / "products.db"
PRODUCTS_JSON = Path(__file__).parent / "products.json"

def init_database():
    """Initialize SQLite database with products table"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def migrate_json_to_db():
    """Migrate products from JSON file to SQLite database"""
    # Check if JSON file exists and database is empty
    if not PRODUCTS_JSON.exists():
        return
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Check if table has data
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    
    if count > 0:
        conn.close()
        print("Database already has products, skipping migration")
        return
    
    # Load from JSON and insert into database
    try:
        with open(PRODUCTS_JSON, "r") as f:
            products = json.load(f)
        
        for product_id, product_data in products.items():
            cursor.execute("""
                INSERT INTO products (id, name, description, price, stock)
                VALUES (?, ?, ?, ?, ?)
            """, (
                int(product_id),
                product_data["name"],
                product_data["description"],
                product_data["price"],
                product_data["stock"]
            ))
        
        conn.commit()
        print(f"Migrated {len(products)} products from JSON to database")
    except Exception as e:
        print(f"Error migrating products: {e}")
    finally:
        conn.close()

def get_all_products():
    """Get all products from database as dictionary"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, description, price, stock FROM products")
    rows = cursor.fetchall()
    conn.close()
    
    # Convert to dictionary format
    products = {}
    for row in rows:
        product_id = str(row["id"])
        products[product_id] = {
            "id": product_id,
            "name": row["name"],
            "description": row["description"],
            "price": row["price"],
            "stock": row["stock"]
        }
    
    return products

def get_product(product_id: int):
    """Get a specific product by ID"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, description, price, stock FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "id": str(row["id"]),
            "name": row["name"],
            "description": row["description"],
            "price": row["price"],
            "stock": row["stock"]
        }
    return None

def create_product(name: str, description: str, price: float, stock: int):
    """Create a new product in database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO products (name, description, price, stock)
        VALUES (?, ?, ?, ?)
    """, (name, description, price, stock))
    
    conn.commit()
    product_id = cursor.lastrowid
    conn.close()
    
    return product_id

def get_next_product_id():
    """Get the next available product ID"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT MAX(id) FROM products")
    result = cursor.fetchone()[0]
    conn.close()
    
    return (result or 0) + 1
