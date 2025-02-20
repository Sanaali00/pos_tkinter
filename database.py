import sqlite3


def init_db():
    conn = sqlite3.connect("pos.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        
        )
    ''')

     cursor.execute('''
         CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT CHECK(role IN ('admin', 'cashier')) NOT NULL
         )
     ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            quantity INTEGER,
            total_price REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

    conn.commit()  # ✅ Save changes
    conn.close()  # ✅ Close connection


# Function to execute INSERT, UPDATE, DELETE queries
def execute_query(query, params=()):
    conn = sqlite3.connect("pos.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()


# Function to fetch data (SELECT queries)
def fetch_data(query, params=()):
    conn = sqlite3.connect("pos.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return data


# Run database initialization when script is executed
if __name__ == "__main__":
    init_db()
    print("✅ Database setup complete. Tables are ready!")
