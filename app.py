# ==========================================
# CAMPUS FOOD ORDERING SYSTEM
# MEMBER 3
# Order History, Search, Data Storage
# Smart Kitchen Queue
# ==========================================

from flask import Flask, request, redirect, render_template
import json
import webbrowser
from datetime import datetime

app = Flask(__name__)

FILE_NAME = "order_history.json"


# ==========================================
# DATA STORAGE
# ==========================================

def load_orders():

    try:

        with open(FILE_NAME, "r") as file:
            orders = json.load(file)

        if isinstance(orders, list):
            return orders

        return []

    except (FileNotFoundError, json.JSONDecodeError):

        return []


def save_orders(orders):

    with open(FILE_NAME, "w") as file:

        json.dump(
            orders,
            file,
            indent=4
        )


# ==========================================
# PREPARE ORDERS
# ==========================================

def prepare_orders(orders):

    changed = False

    for number, order in enumerate(orders):

        if "items" not in order:

            order["items"] = []

            changed = True

        if "table_number" not in order:

            order["table_number"] = (number % 5) + 1

            changed = True

        if "status" not in order:

            order["status"] = "Pending"

            changed = True

        if "order_time" not in order:

            order["order_time"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            changed = True

        if "manual_status" not in order:

            order["manual_status"] = False

            changed = True

    if changed:

        save_orders(orders)

    return orders


# ==========================================
# MERGE ORDERS FROM SAME TABLE
# ==========================================

def merge_table_orders(orders):

    merged_orders = []
    table_positions = {}

    for order in orders:

        table_number = order.get("table_number")

        if table_number not in table_positions:

            table_positions[table_number] = len(
                merged_orders
            )

            merged_orders.append(order)

            continue

        existing_order = merged_orders[
            table_positions[table_number]
        ]

        existing_order.setdefault(
            "items",
            []
        )

        for new_item in order.get("items", []):

            found = False

            for existing_item in existing_order["items"]:

                same_name = (
                    existing_item.get("name")
                    == new_item.get("name")
                )

                same_price = (
                    existing_item.get("price")
                    == new_item.get("price")
                )

                if same_name and same_price:

                    existing_item["quantity"] = (
                        existing_item.get("quantity", 0)
                        + new_item.get("quantity", 0)
                    )

                    found = True

                    break

            if not found:

                existing_order["items"].append(
                    new_item.copy()
                )

        # Recalculate total
        total = 0

        for item in existing_order["items"]:

            total += (
                float(item.get("price", 0))
                * int(item.get("quantity", 0))
            )

        existing_order["total"] = total

        # Keep newest order time
        old_time = existing_order.get(
            "order_time",
            ""
        )

        new_time = order.get(
            "order_time",
            ""
        )

        if new_time > old_time:

            existing_order["order_time"] = new_time

        existing_order["status"] = "Pending"

        existing_order["manual_status"] = False

    if len(merged_orders) != len(orders):

        save_orders(merged_orders)

    return merged_orders


# ==========================================
# AUTOMATIC STATUS UPDATE
# ==========================================

def update_automatic_status(orders):

    changed = False

    for order in orders:

        # Manual status is not changed automatically
        if order.get("manual_status", False):

            continue

        if "order_time" not in order:

            continue

        try:

            order_time = datetime.strptime(
                order["order_time"],
                "%Y-%m-%d %H:%M:%S"
            )

            current_time = datetime.now()

            seconds_passed = (
                current_time - order_time
            ).total_seconds()

            old_status = order.get(
                "status",
                "Pending"
            )

            # ==================================
            # AUTOMATIC STATUS TIMING
            # ==================================

            if seconds_passed < 30:

                new_status = "Pending"

            elif seconds_passed < 60:

                new_status = "Preparing"

            elif seconds_passed < 90:

                new_status = "Ready"

            else:

                new_status = "Completed"

            if old_status != new_status:

                order["status"] = new_status

                changed = True

        except ValueError:

            order["status"] = "Pending"

            changed = True

    if changed:

        save_orders(orders)

    return orders


# ==========================================
# GET CURRENT ORDERS
# ==========================================

def get_orders():

    orders = load_orders()

    orders = prepare_orders(orders)

    orders = merge_table_orders(orders)

    orders = update_automatic_status(orders)

    return orders


# ==========================================
# ORDER SUMMARY
# ==========================================

def get_summary(orders):

    total_orders = len(orders)

    total_sales = 0

    pending = 0
    preparing = 0
    ready = 0
    completed = 0

    for order in orders:

        try:

            total_sales += float(
                order.get("total", 0)
            )

        except (ValueError, TypeError):

            pass

        status = order.get(
            "status",
            "Pending"
        )

        if status == "Pending":

            pending += 1

        elif status == "Preparing":

            preparing += 1

        elif status == "Ready":

            ready += 1

        elif status == "Completed":

            completed += 1

    return {

        "total_orders": total_orders,

        "total_sales": total_sales,

        "pending": pending,

        "preparing": preparing,

        "ready": ready,

        "completed": completed

    }


# ==========================================
# ADD / MERGE NEW ORDER
# ==========================================

def add_order(new_order):

    orders = load_orders()

    orders = prepare_orders(orders)

    table_number = new_order.get(
        "table_number"
    )

    existing_order = None

    for order in orders:

        if order.get("table_number") == table_number:

            existing_order = order

            break

    # ======================================
    # EXISTING TABLE
    # ======================================

    if existing_order is not None:

        existing_order.setdefault(
            "items",
            []
        )

        for new_item in new_order.get(
            "items",
            []
        ):

            found = False

            for existing_item in existing_order["items"]:

                if (
                    existing_item.get("name")
                    == new_item.get("name")
                    and
                    existing_item.get("price")
                    == new_item.get("price")
                ):

                    existing_item["quantity"] = (
                        existing_item.get("quantity", 0)
                        + new_item.get("quantity", 0)
                    )

                    found = True

                    break

            if not found:

                existing_order["items"].append(
                    new_item.copy()
                )

        total = 0

        for item in existing_order["items"]:

            total += (
                float(item.get("price", 0))
                * int(item.get("quantity", 0))
            )

        existing_order["total"] = total

        existing_order["order_time"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        existing_order["status"] = "Pending"

        existing_order["manual_status"] = False

    # ======================================
    # NEW TABLE
    # ======================================

    else:

        new_order["order_time"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        new_order["status"] = "Pending"

        new_order["manual_status"] = False

        orders.append(new_order)

    save_orders(orders)

    return orders


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    orders = get_orders()

    summary = get_summary(orders)

    kitchen_queue = get_kitchen_queue(orders)

    return render_template(
        "index.html",
        orders=orders,
        display_orders=orders,
        search_result=None,
        search_type="food",
        search_value="",
        kitchen_queue=kitchen_queue,
        **summary
    )


# ==========================================
# SELECT SEARCH TYPE
# ==========================================

@app.route(
    "/select_search",
    methods=["POST"]
)
def select_search():

    orders = get_orders()

    search_type = request.form.get(
        "search_type",
        "food"
    )

    summary = get_summary(orders)

    kitchen_queue = get_kitchen_queue(orders)

    return render_template(
        "index.html",
        orders=orders,
        display_orders=orders,
        search_result=None,
        search_type=search_type,
        search_value="",
        kitchen_queue=kitchen_queue,
        **summary
    )


# ==========================================
# SEARCH ORDERS
# ==========================================

@app.route(
    "/search",
    methods=["POST"]
)
def search_order():

    orders = get_orders()

    search_type = request.form.get(
        "search_type",
        "food"
    )

    search_value = request.form.get(
        "search",
        ""
    ).strip()

    search_result = []

    # ======================================
    # SEARCH BY FOOD
    # ======================================

    if search_type == "food":

        search_value_lower = search_value.lower()

        for index, order in enumerate(orders):

            for item in order.get("items", []):

                item_name = str(
                    item.get("name", "")
                ).lower()

                if search_value_lower in item_name:

                    search_result.append({
                        "index": index,
                        "order": order
                    })

                    break

    # ======================================
    # SEARCH BY TABLE
    # ======================================

    elif search_type == "table":

        for index, order in enumerate(orders):

            table_number = str(
                order.get(
                    "table_number",
                    ""
                )
            )

            if table_number == search_value:

                search_result.append({
                    "index": index,
                    "order": order
                })

    # ======================================
    # SEARCH BY STATUS
    # ======================================

    elif search_type == "status":

        for index, order in enumerate(orders):

            order_status = order.get(
                "status",
                "Pending"
            )

            if order_status == search_value:

                search_result.append({
                    "index": index,
                    "order": order
                })

    summary = get_summary(orders)

    kitchen_queue = get_kitchen_queue(orders)

    return render_template(
        "index.html",
        orders=orders,
        display_orders=search_result,
        search_result=search_result,
        search_type=search_type,
        search_value=search_value,
        kitchen_queue=kitchen_queue,
        **summary
    )


# ==========================================
# UPDATE ORDER STATUS
# ==========================================

@app.route(
    "/update_status/<int:order_number>",
    methods=["POST"]
)
def update_status(order_number):

    orders = get_orders()

    if (
        order_number >= 0
        and order_number < len(orders)
    ):

        new_status = request.form.get(
            "status"
        )

        valid_statuses = [
            "Pending",
            "Preparing",
            "Ready",
            "Completed"
        ]

        if new_status in valid_statuses:

            orders[order_number]["status"] = new_status

            # Manual status will not be overwritten
            # by automatic status system
            orders[order_number]["manual_status"] = True

            save_orders(orders)

    return redirect("/")


# ==========================================
# DELETE ORDER
# ==========================================

@app.route(
    "/delete/<int:order_number>"
)
def delete_order(order_number):

    orders = get_orders()

    if (
        order_number >= 0
        and order_number < len(orders)
    ):

        orders.pop(order_number)

        save_orders(orders)

    return redirect("/")


# ==========================================
# SMART KITCHEN QUEUE
# ==========================================

def get_kitchen_queue(orders):

    queue = []

    current_time = datetime.now()

    for order in orders:

        status = order.get(
            "status",
            "Pending"
        )

        # Completed orders leave the queue
        if status == "Completed":

            continue

        try:

            order_time = datetime.strptime(
                order["order_time"],
                "%Y-%m-%d %H:%M:%S"
            )

            waiting_seconds = int(
                (
                    current_time - order_time
                ).total_seconds()
            )

            if waiting_seconds < 0:

                waiting_seconds = 0

        except (KeyError, ValueError):

            waiting_seconds = 0

        # ======================================
        # ESTIMATED REMAINING TIME
        # ======================================

        if status == "Pending":

            estimated_seconds = max(
                90 - waiting_seconds,
                0
            )

        elif status == "Preparing":

            estimated_seconds = max(
                60 - waiting_seconds,
                0
            )

        elif status == "Ready":

            estimated_seconds = 0

        else:

            estimated_seconds = 0

        # ======================================
        # TIME CONVERSION
        # ======================================

        waiting_minutes = (
            waiting_seconds // 60
        )

        waiting_remaining_seconds = (
            waiting_seconds % 60
        )

        estimated_minutes = (
            estimated_seconds // 60
        )

        estimated_remaining_seconds = (
            estimated_seconds % 60
        )

        # ======================================
        # ADD TO QUEUE
        # ======================================

        queue.append({

            "table_number": order.get(
                "table_number",
                ""
            ),

            "status": status,

            "waiting_minutes": waiting_minutes,

            "waiting_seconds": (
                waiting_remaining_seconds
            ),

            "estimated_minutes": estimated_minutes,

            "estimated_seconds": (
                estimated_remaining_seconds
            ),

            "order_time": order.get(
                "order_time",
                ""
            )

        })

    # ======================================
    # QUEUE PRIORITY
    # ======================================

    # Pending / Preparing orders first.
    # Older orders first.
    # Ready orders appear after active preparation.
    queue.sort(
        key=lambda order: (
            order["status"] == "Ready",
            order["order_time"]
        )
    )

    return queue


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    import threading

    def open_browser():

        webbrowser.open(
            "http://127.0.0.1:5000"
        )

    # Open browser shortly after Flask starts
    threading.Timer(
        1.5,
        open_browser
    ).start()

    app.run(
        debug=False,
        use_reloader=False
    )