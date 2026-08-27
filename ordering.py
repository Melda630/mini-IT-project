#CAMPUS FOOD ORDERING SYSTEM

cart = []


def add_to_cart(item_name, price, quantity):
    """Add a food item to the cart."""

    if quantity <= 0:
        print("Quantity must be greater than 0.")
        return

    # Check if item already exists in cart
    for item in cart:
        if item["name"] == item_name:
            item["quantity"] += quantity
            print(f"{item_name} quantity updated.")
            return

    # Add new item
    cart.append({
        "name": item_name,
        "price": price,
        "quantity": quantity
    })

    print(f"{item_name} added to cart.")


def view_cart():
    """Display all items currently in the cart."""

    if not cart:
        print("\nYour cart is empty.")
        return

    print("\n========== YOUR CART ==========")

    for i, item in enumerate(cart, start=1):
        subtotal = item["price"] * item["quantity"]

        print(
            f"{i}. {item['name']} "
            f"x {item['quantity']} "
            f"@ RM{item['price']:.2f} "
            f"= RM{subtotal:.2f}"
        )

    print("-------------------------------")
    print(f"TOTAL: RM{calculate_total():.2f}")


def calculate_total():
    """Calculate the total price of all items in the cart."""

    total = 0

    for item in cart:
        total += item["price"] * item["quantity"]

    return total


def modify_quantity(item_number, new_quantity):
    """Modify the quantity of an item in the cart."""

    if not cart:
        print("Cart is empty.")
        return

    if item_number < 1 or item_number > len(cart):
        print("Invalid item number.")
        return

    if new_quantity <= 0:
        print("Quantity must be greater than 0.")
        return

    cart[item_number - 1]["quantity"] = new_quantity

    print("Quantity updated successfully.")


def remove_item(item_number):
    """Remove an item from the cart."""

    if not cart:
        print("Cart is empty.")
        return

    if item_number < 1 or item_number > len(cart):
        print("Invalid item number.")
        return

    removed_item = cart.pop(item_number - 1)

    print(f"{removed_item['name']} removed from cart.")


def checkout():
    """Confirm the order and display the final total."""

    if not cart:
        print("\nCannot checkout. Your cart is empty.")
        return

    print("\n========== CHECKOUT ==========")

    view_cart()

    confirmation = input("\nConfirm order? (Y/N): ").upper()

    if confirmation == "Y":
        print("\nOrder confirmed!")
        print(f"Total amount: RM{calculate_total():.2f}")

        # Clear cart after successful checkout
        cart.clear()

    else:
        print("\nOrder cancelled.")