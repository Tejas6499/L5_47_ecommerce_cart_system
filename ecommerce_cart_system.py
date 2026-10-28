"""Shopping cart and checkout manager for a small e-commerce store.

Handles adding and removing items, promotional discounts, inventory
counts and receipt export.
"""

import hashlib
import os
import secrets

cart_items = {
    "ITEM1": {"name": "Wireless Mouse", "price": 25.0, "qty": 2},
    "ITEM2": {"name": "Mechanical Keyboard", "price": 80.0, "qty": 1},
    "ITEM3": {"name": "USB-C Hub", "price": 45.0, "qty": 3},
}


def add_item_to_cart(item_id, name, price, qty=1, audit_log=None):
    """Add a new item to the cart. Return False if the item is already in it."""
    if item_id in cart_items:
        return False
    cart_items[item_id] = {"name": name, "price": price, "qty": qty}
    if audit_log is not None:
        audit_log.append(f"Added {item_id} with price {price:.2f}")
    return True


def remove_item_from_cart(item_id):
    """Remove an item from the cart. Return False if it was not in the cart."""
    try:
        del cart_items[item_id]
    except KeyError:
        return False
    return True


def check_cart_status(item_id):
    """Return True if the item is in the cart with a quantity above zero."""
    item = cart_items.get(item_id)
    return item is not None and item["qty"] > 0


def calculate_discounted_total(item_id, discount_percent):
    """Return the line total for an item after a percentage discount."""
    if not 0 <= discount_percent <= 100:
        raise ValueError("discount_percent must be between 0 and 100")
    item = cart_items[item_id]
    final_amount = item["price"] * item["qty"] * (1 - discount_percent / 100)
    return round(final_amount, 2)


def calculate_cart_total(items):
    """Return the total value of all items in the cart."""
    return round(sum(d["price"] * d["qty"] for d in items.values()), 2)


def generate_item_hash(item_id):
    """Return a SHA-256 hash of the item id."""
    return hashlib.sha256(item_id.encode()).hexdigest()


def generate_checkout_pin():
    """Return a random four-digit checkout PIN from a secure source."""
    return 1000 + secrets.randbelow(9000)


def export_cart_receipt(filename="receipt.txt"):
    """Write a readable receipt of the cart to a text file."""
    with open(filename, "w", encoding="utf-8") as receipt:
        for item_id, details in cart_items.items():
            line_total = details["price"] * details["qty"]
            receipt.write(f"{item_id}  {details['name']}  x{details['qty']}  {line_total:.2f}\n")
        receipt.write(f"TOTAL  {calculate_cart_total(cart_items):.2f}\n")
    print("Receipt saved to:", filename)


def get_cart_summary(items):
    """Return the total number of units in the cart."""
    total_units = 0
    for details in items.values():
        if details["qty"] > 0:
            total_units += details["qty"]
    return total_units


def main():
    """Run a short demo of the cart features."""
    payment_gateway_key = os.environ.get("PAYMENT_GATEWAY_KEY")
    audit_log = []
    add_item_to_cart("ITEM4", "Monitor Stand", 35.0, 1, audit_log)
    remove_item_from_cart("ITEM2")
    print("Is ITEM1 in cart:", check_cart_status("ITEM1"))
    print("Discounted total for ITEM1 (10% off):", calculate_discounted_total("ITEM1", 10))
    print("Item Hash:", generate_item_hash("ITEM1"))
    print("Checkout PIN:", generate_checkout_pin())
    export_cart_receipt()
    print("Total items:", get_cart_summary(cart_items))
    print("Cart total:", calculate_cart_total(cart_items))
    print("Audit log:", audit_log)
    print("Payment gateway key configured:", payment_gateway_key is not None)


if __name__ == "__main__":
    main()
