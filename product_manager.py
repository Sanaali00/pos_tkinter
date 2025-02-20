from database import execute_query, fetch_data

def add_product(name, price, stock):
    """Adds a new product to the database."""
    execute_query("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
    print(f"Product '{name}' added successfully!")

def update_product(product_id, name, price, stock):
    """Updates an existing product."""
    execute_query("UPDATE products SET name")
    print(f"Product '{name},{product_id},{price},{stock}'updated successfully!")