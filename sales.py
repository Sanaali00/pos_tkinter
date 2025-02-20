from database import execute_query, fetch_data
from datetime import datetime


def add_to_cart(cart, product_id, quantity):
    """Adds a product to the shopping cart."""
    product = fetch_data("SELECT name, price, stock FROM products WHERE id = ?", (product_id,))

    if not product:
        print("Product not found.")
        return False

    name, price, stock = product[0]

    if quantity > stock:
        print("Not enough stock available.")
        return False

    cart.append({"id": product_id, "name": name, "price": price, "quantity": quantity})
    print(f"Added {quantity} of {name} to cart.")
    return True


def calculate_total(cart):
    """Calculates the total amount."""
    return sum(item["price"] * item["quantity"] for item in cart)


def checkout(cart):
    """Processes the checkout, updates stock, and stores sales records."""
    if not cart:
        print("Cart is empty. Cannot checkout.")
        return False

    total = calculate_total(cart)
    print(f"Total Amount: ${total:.2f}")

    confirmation = input("Confirm payment? (yes/no): ")
    if confirmation.lower() != 'yes':
        print("Checkout cancelled.")
        return False

    for item in cart:
        execute_query("INSERT INTO sales (product_id, quantity, total_price, date) VALUES (?, ?, ?, ?)",
                      (item["id"], item["quantity"], item["price"] * item["quantity"],
                       datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        execute_query("UPDATE products SET stock = stock - ? WHERE id = ?", (item["quantity"], item["id"]))

    print("Purchase successful! Thank you.")
    cart.clear()
    return True
