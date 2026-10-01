import json
from datetime import datetime, timedelta

FILE_NAME = "order_history.json"


# Load all orders from JSON file
def load_history():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# Save all orders into JSON file
def save_history(orders):
    with open(FILE_NAME, "w") as file:
        json.dump(orders, file, indent=4)


# Generate Order ID
# Order ID resets every new day
def generate_order_id():
    orders = load_history()
    today = datetime.now().strftime("%Y-%m-%d")
    highest = 0

    for order in orders:
        if order.get("date") == today:
            try:
                number = int(
                    order["order_id"].replace("ORD", "")
                )
                highest = max(highest, number)
            except (ValueError, KeyError):
                pass

    return f"ORD{highest + 1:04d}"


# Add a new checkout into order history
def add_history(table_number, order):
    orders = load_history()
    now = datetime.now()

    new_order = {
        "order_id": generate_order_id(),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "completed_time": None,
        "order_type": order["order_type"],
        "table_number": table_number,
        "items": order["items"],
        "total": order["total"],
        "status": "Ongoing"
    }

    orders.append(new_order)
    save_history(orders)

    return new_order


# Customer: show today's ongoing orders for a table
def get_current_table_orders(table_number):
    orders = load_history()
    today = datetime.now().strftime("%Y-%m-%d")
    results = []

    for order in orders:
        if (
            order.get("order_type") == "Dine In"
            and str(order.get("table_number")) == str(table_number)
            and order.get("date") == today
            and order.get("status") == "Ongoing"
        ):
            results.append(order)

    return results


# Search using Order ID and date
def search_by_order_id(order_id, order_date=None):
    orders = load_history()
    results = []

    for order in orders:
        if order.get("order_id", "").lower() == order_id.lower():

            if order_date is None or order.get("date") == order_date:
                results.append(order)

    return results


# Admin: get every order from a selected date
def search_by_date(order_date):
    orders = load_history()
    results = []

    for order in orders:
        if order.get("date") == order_date:
            results.append(order)

    return results


# Admin: search history by table
def search_by_table(table_number):
    orders = load_history()
    results = []

    for order in orders:
        if str(order.get("table_number")) == str(table_number):
            results.append(order)

    return results


# Get orders from today and previous 4 days
def get_last_5_days():
    orders = load_history()

    today = datetime.now().date()
    start_date = today - timedelta(days=4)

    results = []

    for order in orders:
        try:
            order_date = datetime.strptime(
                order["date"],
                "%Y-%m-%d"
            ).date()

            if start_date <= order_date <= today:
                results.append(order)

        except (ValueError, KeyError):
            pass

    return results


# Admin manually changes order status
def update_history(order_id, order_date, new_status):
    if new_status not in ["Ongoing", "Completed"]:
        return False

    orders = load_history()

    for order in orders:
        if (
            order.get("order_id") == order_id
            and order.get("date") == order_date
        ):

            order["status"] = new_status

            # Record time when cash payment is completed
            if new_status == "Completed":
                order["completed_time"] = (
                    datetime.now().strftime("%H:%M:%S")
                )
            else:
                order["completed_time"] = None

            save_history(orders)
            return True

    return False


# Complete all ongoing orders for one dine-in table
def complete_table_orders(table_number):
    orders = load_history()
    today = datetime.now().strftime("%Y-%m-%d")
    completed_time = datetime.now().strftime("%H:%M:%S")

    updated = False

    for order in orders:
        if (
            order.get("order_type") == "Dine In"
            and str(order.get("table_number")) == str(table_number)
            and order.get("date") == today
            and order.get("status") == "Ongoing"
        ):

            order["status"] = "Completed"
            order["completed_time"] = completed_time
            updated = True

    if updated:
        save_history(orders)

    return updated


# Delete an order from history
def delete_history(order_id, order_date):
    orders = load_history()

    for order in orders:
        if (
            order.get("order_id") == order_id
            and order.get("date") == order_date
        ):
            orders.remove(order)
            save_history(orders)
            return True

    return False


# Calculate completed sales only
def calculate_sales(orders):
    total = 0

    for order in orders:
        if order.get("status") == "Completed":
            total += order.get("total", 0)

    return total


# Calculate current total for a dine-in table
def calculate_table_total(orders):
    total = 0

    for order in orders:
        total += order.get("total", 0)

    return total


# Admin: daily summary for last 5 days
def get_daily_summary():
    orders = get_last_5_days()

    today = datetime.now().date()
    summary = []

    for day_number in range(5):
        current_date = today - timedelta(days=day_number)
        date_text = current_date.strftime("%Y-%m-%d")

        total_orders = 0
        completed_orders = 0
        ongoing_orders = 0
        total_sales = 0

        for order in orders:
            if order.get("date") == date_text:

                total_orders += 1

                if order.get("status") == "Completed":
                    completed_orders += 1
                    total_sales += order.get("total", 0)

                elif order.get("status") == "Ongoing":
                    ongoing_orders += 1

        summary.append({
            "date": date_text,
            "total_orders": total_orders,
            "completed_orders": completed_orders,
            "ongoing_orders": ongoing_orders,
            "total_sales": total_sales
        })

    return summary