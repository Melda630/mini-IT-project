#CAMPUS FOOD ORDERING SYSTEM

cart = []
order_history = []


def add_to_cart(item_name, price, quantity):
    if quantity <= 0:
        print("Invalid quantity. Please enter a quantity greater than 0.")
        return

    # If item already exists, increase quantity
    for item in cart:
        if item["name"] == item_name:
            item["quantity"] += quantity
            print(f"{item_name} quantity updated to {item['quantity']}.")
            return

    item = {
        "name": item_name,
        "price": price,
        "quantity": quantity
    }

    cart.append(item)
    print(f"{item_name} x{quantity} added to cart.")


def view_cart():
    if len(cart) == 0:
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
    print("================================")


def calculate_total():
    total = 0

    for item in cart:
        total += item["price"] * item["quantity"]

    return total


def modify_quantity(item_number, new_quantity):
    if len(cart) == 0:
        print("Cart is empty.")
        return

    if item_number < 1 or item_number > len(cart):
        print("Invalid item number.")
        return

    if new_quantity <= 0:
        print("Invalid quantity. Please enter a quantity greater than 0.")
        return

    cart[item_number - 1]["quantity"] = new_quantity

    print(
        f"{cart[item_number - 1]['name']} quantity updated to "
        f"{new_quantity}."
    )


def remove_item(item_number):
    if len(cart) == 0:
        print("Cart is empty.")
        return

    if item_number < 1 or item_number > len(cart):
        print("Invalid item number.")
        return

    removed_item = cart.pop(item_number - 1)

    print(f"{removed_item['name']} removed from cart.")


def clear_cart():
    if len(cart) == 0:
        print("Cart is already empty.")
        return

    cart.clear()
    print("Cart cleared.")


def checkout():
    if len(cart) == 0:
        print("\nCannot checkout. Your cart is empty.")
        return

    print("\n========== CHECKOUT ==========")

    view_cart()

    while True:
        confirm = input("\nConfirm order? (Y/N): ").strip().upper()

        if confirm == "Y":

            completed_order = {
                "items": [],
                "total": calculate_total()
            }

            for item in cart:
                completed_order["items"].append(item.copy())

            order_history.append(completed_order)

            print("\nOrder confirmed!")
            print(f"Final total: RM{calculate_total():.2f}")

            cart.clear()

            break

        elif confirm == "N":
            print("\nOrder cancelled.")
            break

        else:
            print("Invalid input. Please enter Y or N.")


def view_order_history():
    if len(order_history) == 0:
        print("\nNo order history available.")
        return

    print("\n========== ORDER HISTORY ==========")

    for order_number, order in enumerate(order_history, start=1):

        print(f"\nOrder {order_number}")

        for item in order["items"]:

            subtotal = item["price"] * item["quantity"]

            print(
                f"{item['name']} "
                f"x {item['quantity']} "
                f"= RM{subtotal:.2f}"
            )

        print(f"Total: RM{order['total']:.2f}")

    print("===================================")
