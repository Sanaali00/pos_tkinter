import tkinter as tk
from tkinter import messagebox, ttk
from database import fetch_data, execute_query


class POSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Point of Sale System")
        self.root.geometry("700x600")
        self.root.configure(bg="#f4f4f4")

        self.create_main_menu()

    def create_main_menu(self):
        """Creates the main menu to navigate between pages."""
        tk.Label(self.root, text="POS SYSTEM", font=("Arial", 16, "bold"), bg="#4CAF50", fg="white", padx=10,
                 pady=5).pack(fill="x")

        tk.Button(self.root, text="Product Management", command=self.open_product_management, font=("Arial", 12),
                  bg="#2196F3", fg="white").pack(pady=10)
        tk.Button(self.root, text="Sales Processing", command=self.open_sales_processing, font=("Arial", 12),
                  bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(self.root, text="Store Sales & Print Receipt", command=self.open_store_sales, font=("Arial", 12),
                  bg="#FF9800", fg="white").pack(pady=10)

    def open_product_management(self):
        self.new_window(ProductManagement)

    def open_sales_processing(self):
        self.new_window(SalesProcessing)

    def open_store_sales(self):
        self.new_window(StoreSales)

    def new_window(self, window_class):
        new_win = tk.Toplevel(self.root)
        window_class(new_win)


class ProductManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Management")
        self.root.geometry("700x500")

        tk.Label(root, text="Product Management", font=("Arial", 16, "bold"), bg="#4CAF50", fg="white", padx=10,
                 pady=5).pack(fill="x")

        self.product_name_var = tk.StringVar()
        self.product_price_var = tk.DoubleVar()
        self.product_stock_var = tk.IntVar()

        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Product Name:").grid(row=0, column=0)
        tk.Entry(frame, textvariable=self.product_name_var, width=20).grid(row=0, column=1)

        tk.Label(frame, text="Price:").grid(row=0, column=2)
        tk.Entry(frame, textvariable=self.product_price_var, width=10).grid(row=0, column=3)

        tk.Label(frame, text="Stock:").grid(row=0, column=4)
        tk.Entry(frame, textvariable=self.product_stock_var, width=10).grid(row=0, column=5)

        tk.Button(frame, text="Add Product", command=self.add_product, bg="#4CAF50", fg="white").grid(row=0, column=6)
        tk.Button(frame, text="Update", command=self.update_product, bg="#FFC107").grid(row=0, column=7)
        tk.Button(frame, text="Delete", command=self.delete_product, bg="#F44336", fg="white").grid(row=0, column=8)

        self.product_list = ttk.Treeview(root, columns=("Name", "Price", "Stock"), show="headings")
        self.product_list.heading("Name", text="Product Name")
        self.product_list.heading("Price", text="Price")
        self.product_list.heading("Stock", text="Stock")
        self.product_list.pack(fill="both", expand=True, padx=20, pady=10)

        self.load_product_list()


    def load_product_list(self):
        self.product_list.delete(*self.product_list.get_children())
        products = fetch_data("SELECT name, price, stock FROM products")
        for name, price, stock in products:
            self.product_list.insert("", "end", values=(name, price, stock))

    def add_product(self):
        name, price, stock = self.product_name_var.get(), self.product_price_var.get(), self.product_stock_var.get()
        if name and price > 0 and stock >= 0:
            execute_query("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
            self.load_product_list()
            messagebox.showinfo("Success", "Product Added Successfully")
        else:
            messagebox.showwarning("Invalid Input", "Please enter valid product details!")

    def update_product(self):
        selected_item = self.product_list.selection()
        if selected_item:
            name = self.product_list.item(selected_item, "values")[0]
            execute_query("UPDATE products SET price=?, stock=? WHERE name=?",
                          (self.product_price_var.get(), self.product_stock_var.get(), name))
            self.load_product_list()
            messagebox.showinfo("Success", "Product Updated Successfully")
        else:
            messagebox.showwarning("Selection Error", "Select a product to update!")

    def delete_product(self):
        selected_item = self.product_list.selection()
        if selected_item:
            name = self.product_list.item(selected_item, "values")[0]
            execute_query("DELETE FROM products WHERE name=?", (name,))
            self.load_product_list()
            messagebox.showinfo("Success", "Product Deleted Successfully")
        else:
            messagebox.showwarning("Selection Error", "Select a product to delete!")


class SalesProcessing:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Processing")
        self.root.geometry("700x500")
        tk.Label(root, text="Sales Processing", font=("Arial", 16, "bold"), bg="#4CAF50", fg="white", padx=10,
                 pady=5).pack(fill="x")

        self.cart = {}  # Shopping cart
        self.products = self.load_products()  # Load products from DB

        # Header Label
        tk.Label(root, text="POS SYSTEM", font=("Arial", 16, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5).pack(
            fill="x")

        # Product Selection
        self.product_frame = tk.Frame(root, bg="#ffffff", pady=10)
        self.product_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(self.product_frame, text="Select Product:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.product_var = tk.StringVar()
        self.product_dropdown = ttk.Combobox(self.product_frame, textvariable=self.product_var, state="readonly",
                                             width=15)
        self.product_dropdown.grid(row=0, column=1, padx=5)
        self.update_product_dropdown()

        tk.Label(self.product_frame, text="Quantity:", font=("Arial", 12)).grid(row=0, column=2, padx=5)
        self.qty_var = tk.IntVar(value=1)
        self.qty_entry = tk.Entry(self.product_frame, textvariable=self.qty_var, width=5)
        self.qty_entry.grid(row=0, column=3, padx=5)

        self.add_button = tk.Button(self.product_frame, text="Add to Cart", command=self.add_to_cart, bg="#4CAF50",
                                    fg="white", font=("Arial", 10, "bold"))
        self.add_button.grid(row=0, column=4, padx=10)

        # Cart Display
        tk.Label(root, text="Shopping Cart", font=("Arial", 14, "bold")).pack()
        self.cart_display = tk.Text(root, height=10, width=60, state="disabled")
        self.cart_display.pack(pady=5)

        # Checkout & Receipt
        self.checkout_button = tk.Button(root, text="Checkout", command=self.checkout, bg="#008CBA", fg="white",
                                         font=("Arial", 12, "bold"))
        self.checkout_button.pack(pady=5)

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
            self.cart_display.insert(tk.END,
                                     f"{item} x {details['quantity']} = ${details['price'] * details['quantity']:.2f}\n")

        self.cart_display.config(state="disabled")

    def checkout(self):
        """Deducts stock, saves transaction, and clears the cart."""
        if not self.cart:
            messagebox.showwarning("Empty Cart", "No items in the cart!")
            return

        total_price = sum(item["quantity"] * item["price"] for item in self.cart.values())

        for product, details in self.cart.items():
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




class StoreSales:
    def __init__(self, root):
        self.root = root
        self.root.title("Store Sales & Print Receipt")
        self.root.geometry("700x500")
        tk.Label(root, text="Store Sales & Print Receipt", font=("Arial", 16, "bold"), bg="#FF9800", fg="white",
                 padx=10, pady=5).pack(fill="x")

        # Add store sales tracking and receipt printing features here


if __name__ == "__main__":
    root = tk.Tk()
    app = POSApp(root)
    root.mainloop()
