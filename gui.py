import tkinter as tk
from tkinter import messagebox, ttk
from database import fetch_data, execute_query

class POSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Point of Sale System")
        self.root.geometry("600x500")
        self.root.configure(bg="#f4f4f4")

        self.cart = {}  # Shopping cart
        self.products = self.load_products()  # Load products from DB

        # Header Label
        tk.Label(root, text="POS SYSTEM", font=("Arial", 16, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5).pack(fill="x")

        # Product Selection
        self.product_frame = tk.Frame(root, bg="#ffffff", pady=10)
        self.product_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(self.product_frame, text="Select Product:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.product_var = tk.StringVar()
        self.product_dropdown = ttk.Combobox(self.product_frame, textvariable=self.product_var, state="readonly", width=15)
        self.product_dropdown.grid(row=0, column=1, padx=5)
        self.update_product_dropdown()

        tk.Label(self.product_frame, text="Quantity:", font=("Arial", 12)).grid(row=0, column=2, padx=5)
        self.qty_var = tk.IntVar(value=1)
        self.qty_entry = tk.Entry(self.product_frame, textvariable=self.qty_var, width=5)
        self.qty_entry.grid(row=0, column=3, padx=5)

        self.add_button = tk.Button(self.product_frame, text="Add to Cart", command=self.add_to_cart, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.add_button.grid(row=0, column=4, padx=10)

        # Cart Display
        tk.Label(root, text="Shopping Cart", font=("Arial", 14, "bold")).pack()
        self.cart_display = tk.Text(root, height=10, width=60, state="disabled")
        self.cart_display.pack(pady=5)

        # Checkout & Receipt
        self.checkout_button = tk.Button(root, text="Checkout", command=self.checkout, bg="#008CBA", fg="white", font=("Arial", 12, "bold"))
        self.checkout_button.pack(pady=5)

        self.print_receipt_button = tk.Button(root, text="Print Receipt", command=self.print_receipt, bg="#FF5722", fg="white", font=("Arial", 12, "bold"))
        self.print_receipt_button.pack(pady=5)


    def load_products(self):
        """Load products from the database."""
        products_data = fetch_data("SELECT name, price, stock FROM products")
        return {name: {"price": price, "stock": stock} for name, price, stock in products_data}

    def update_product_dropdown(self):
        """Update dropdown list with products from the database."""
        self.product_dropdown["values"] = list(self.products.keys())

    def add_to_cart(self):
        """Add selected product to cart if stock is available."""
        product = self.product_var.get()
        quantity = self.qty_var.get()

        if not product or quantity <= 0:
            messagebox.showwarning("Invalid Entry", "Select a product and enter a valid quantity!")
            return

        # Check stock availability
        available_stock = self.products[product]["stock"]
        if quantity > available_stock:
            messagebox.showwarning("Out of Stock", f"Only {available_stock} units available.")
            return

        # Add to cart
        if product in self.cart:
            self.cart[product]["quantity"] += quantity
        else:
            self.cart[product] = {"quantity": quantity, "price": self.products[product]["price"]}

        self.update_cart_display()

    def update_cart_display(self):
        """Updates the shopping cart display."""
        self.cart_display.config(state="normal")
        self.cart_display.delete(1.0, tk.END)

        for item, details in self.cart.items():
            self.cart_display.insert(tk.END, f"{item} x {details['quantity']} = ${details['price'] * details['quantity']:.2f}\n")

        self.cart_display.config(state="disabled")

    def checkout(self):
        """Deducts stock, saves transaction, and clears the cart."""
        if not self.cart:
            messagebox.showwarning("Empty Cart", "No items in the cart!")
            return

        total_price = sum(item["quantity"] * item["price"] for item in self.cart.values())

        for product, details in self.cart.items():
            # Deduct stock from database
            execute_query("UPDATE products SET stock = stock - ? WHERE name = ?", (details["quantity"], product))

            # Record Sale
            product_id = fetch_data("SELECT id FROM products WHERE name = ?", (product,))[0][0]
            execute_query("INSERT INTO sales (product_id, quantity, total_price) VALUES (?, ?, ?)",
                          (product_id, details["quantity"], details["quantity"] * details["price"]))

        messagebox.showinfo("Checkout", f"Total: ${total_price:.2f}\nTransaction Completed.")

        # Refresh product data
        self.products = self.load_products()
        self.update_product_dropdown()
        self.cart = {}
        self.update_cart_display()

    def print_receipt(self):
        """Generates and prints receipt."""
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Add items to cart before printing receipt.")
            return

        total = sum(item["quantity"] * item["price"] for item in self.cart.values())
        receipt = ReceiptGenerator()
        receipt_text = receipt.generate_receipt(self.cart, total, "Cash")
        messagebox.showinfo("Receipt", receipt_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = POSApp(root)
    root.mainloop()
