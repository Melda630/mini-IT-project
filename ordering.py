#CAMPUS FOOD ORDERING SYSTEM

cart = []
order_history = []


def add_to_cart(item_name, price, quantity):
    if quantity <= 0:
        return False

    for item in cart:
        if item["name"] == item_name:
            item["quantity"] += quantity
            return True

    cart.append({
        "name": item_name,
        "price": price,
        "quantity": quantity
    })

    return True


def calculate_total():
    total = 0

    for item in cart:
        total += item["price"] * item["quantity"]

    return total


def modify_quantity(item_number, new_quantity):
    if item_number < 1 or item_number > len(cart):
        return False

    if new_quantity <= 0:
        return False

    cart[item_number - 1]["quantity"] = new_quantity
    return True


def remove_item(item_number):
    if item_number < 1 or item_number > len(cart):
        return False

    cart.pop(item_number - 1)
    return True


def checkout():
    if len(cart) == 0:
        return False

    completed_order = {
        "items": [],
        "total": calculate_total()
    }

    for item in cart:
        completed_order["items"].append(item.copy())

    order_history.append(completed_order)

    cart.clear()

    return True


def clear_cart():
    cart.clear()