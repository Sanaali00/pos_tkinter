from database import fetch_data

import datetime


class ReceiptGenerator:
    def __init__(self, receipt_file="receipts.txt"):
        self.receipt_file = receipt_file

    def generate_receipt(self, cart_items, total_amount, payment_method):
        """Generates and saves a receipt."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        receipt_content = f"\n===== RECEIPT =====\nDate: {timestamp}\n"

        for item, details in cart_items.items():
            receipt_content += f"{item} x {details['quantity']} = ${details['price'] * details['quantity']:.2f}\n"

        receipt_content += f"\nTotal: ${total_amount:.2f}\nPayment: {payment_method}\n"
        receipt_content += "===================\n"

        with open(self.receipt_file, "a") as file:
            file.write(receipt_content)

        return receipt_content


# Example Usage:
if __name__ == "__main__":
    receipt = ReceiptGenerator()
    sample_cart = {"Apple": {"quantity": 2, "price": 1.5}, "Banana": {"quantity": 3, "price": 1.0}}
    print(receipt.generate_receipt(sample_cart, 6.0, "Cash"))

