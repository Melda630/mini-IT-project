# ==========================================
# CAMPUS FOOD ORDERING SYSTEM
# MEMBER 3
# Order History, Search, Data Storage & Testing
# ==========================================

from flask import Flask, request, redirect
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
        file = open(FILE_NAME, "r")
        orders = json.load(file)
        file.close()
        return orders

    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_orders(orders):
    file = open(FILE_NAME, "w")
    json.dump(orders, file, indent=4)
    file.close()


# ==========================================
# PREPARE OLD ORDERS
# ==========================================

def prepare_orders(orders):
    """
    Adds missing information to old orders.

    This allows the new system to work with
    orders created before the new features
    were added.
    """

    changed = False

    for number, order in enumerate(orders):

        # Add table number if missing
        if "table_number" not in order:
            order["table_number"] = (number % 5) + 1
            changed = True

        # Add status if missing
        if "status" not in order:
            order["status"] = "Pending"
            changed = True

        # Add order time if missing
        if "order_time" not in order:
            order["order_time"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            changed = True

    if changed:
        save_orders(orders)

    return orders


# ==========================================
# AUTOMATIC STATUS UPDATE
# ==========================================

def update_automatic_status(orders):
    """
    Automatically updates order status based
    on how much time has passed.

    0-30 seconds   = Pending
    30-60 seconds  = Preparing
    60-90 seconds  = Ready
    90+ seconds    = Completed

    These short times are used for demonstration
    and testing purposes.
    """

    changed = False

    for order in orders:

        if "order_time" not in order:
            continue

        # Do not change manually completed orders
        if order.get("status") == "Completed":
            continue

        try:
            order_time = datetime.strptime(
                order["order_time"],
                "%Y-%m-%d %H:%M:%S"
            )

            current_time = datetime.now()

            time_passed = (
                current_time - order_time
            ).total_seconds()

            old_status = order.get("status", "Pending")

            if time_passed < 30:
                new_status = "Pending"

            elif time_passed < 60:
                new_status = "Preparing"

            elif time_passed < 90:
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
# FRONTEND PAGE
# ==========================================

def create_page(
    orders,
    search_result=None,
    search_type=None,
    search_value=None
):

    html = """
    <!DOCTYPE html>

    <html>

    <head>

        <title>Campus Food Ordering System</title>

        <style>

            body {
                font-family: Arial;
                background-color: #f2f2f2;
                margin: 0;
                padding: 20px;
            }

            h1 {
                text-align: center;
            }

            .container {
                max-width: 1000px;
                margin: auto;
            }

            .box {
                background: white;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 10px;
            }

            .summary {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }

            .summary-box {
                background: #eeeeee;
                padding: 15px;
                border-radius: 8px;
                flex: 1;
                min-width: 130px;
                text-align: center;
            }

            input, select, button {
                padding: 10px;
                margin: 5px;
            }

            button {
                cursor: pointer;
            }

            .order {
                border: 1px solid #cccccc;
                padding: 15px;
                margin-top: 15px;
                border-radius: 8px;
            }

            .status {
                font-weight: bold;
                font-size: 18px;
            }

            .delete {
                color: red;
                text-decoration: none;
            }

            .item {
                margin-left: 20px;
            }

        </style>

    </head>

    <body>

    <div class="container">

        <h1>Campus Food Ordering System</h1>

        <div class="box">

            <h2>Order Summary</h2>

            <div class="summary">

                <div class="summary-box">
                    <h3>{{ total_orders }}</h3>
                    <p>Total Orders</p>
                </div>

                <div class="summary-box">
                    <h3>RM {{ "%.2f"|format(total_sales) }}</h3>
                    <p>Total Sales</p>
                </div>

                <div class="summary-box">
                    <h3>{{ pending }}</h3>
                    <p>Pending</p>
                </div>

                <div class="summary-box">
                    <h3>{{ preparing }}</h3>
                    <p>Preparing</p>
                </div>

                <div class="summary-box">
                    <h3>{{ ready }}</h3>
                    <p>Ready</p>
                </div>

                <div class="summary-box">
                    <h3>{{ completed }}</h3>
                    <p>Completed</p>
                </div>

            </div>

        </div>


        <div class="box">

            <h2>Search Orders</h2>

            <form method="POST" action="/search">

                <select name="search_type">

                    <option value="food"
                    {% if search_type == "food" %}selected{% endif %}>
                        Food Name
                    </option>

                    <option value="table"
                    {% if search_type == "table" %}selected{% endif %}>
                        Table Number
                    </option>

                    <option value="status"
                    {% if search_type == "status" %}selected{% endif %}>
                        Order Status
                    </option>

                </select>


                <input
                    type="text"
                    name="search"
                    value="{{ search_value or '' }}"
                    placeholder="Enter search..."
                    required
                >

                <button type="submit">
                    Search
                </button>

            </form>

        </div>


        {% if search_result is not none %}

        <div class="box">

            <h2>Search Results</h2>

            {% if search_result %}

                {% for order in search_result %}

                <div class="order">

                    <h3>
                        Table {{ order.table_number }}
                    </h3>

                    <p>
                        <b>Status:</b>
                        <span class="status">
                            {{ order.status }}
                        </span>
                    </p>

                    <p>
                        <b>Order Time:</b>
                        {{ order.order_time }}
                    </p>

                    <p><b>Items:</b></p>

                    {% for item in order.items %}

                    <p class="item">

                        {{ item.name }}
                        x {{ item.quantity }}

                        -
                        RM {{ "%.2f"|format(item.price * item.quantity) }}

                    </p>

                    {% endfor %}

                    <p>
                        <b>Total:</b>
                        RM {{ "%.2f"|format(order.total) }}
                    </p>

                </div>

                {% endfor %}

            {% else %}

                <p>No matching orders found.</p>

            {% endif %}

        </div>

        {% endif %}


        <div class="box">

            <h2>All Order History</h2>

            {% if orders %}

                {% for order in orders %}

                <div class="order">

                    <h3>
                        Table {{ order.table_number }}
                    </h3>

                    <p>
                        <b>Status:</b>
                        <span class="status">
                            {{ order.status }}
                        </span>
                    </p>

                    <p>
                        <b>Order Time:</b>
                        {{ order.order_time }}
                    </p>


                    <p><b>Items:</b></p>

                    {% for item in order.items %}

                    <p class="item">

                        {{ item.name }}
                        x {{ item.quantity }}

                        -
                        RM {{ "%.2f"|format(item.price * item.quantity) }}

                    </p>

                    {% endfor %}


                    <p>

                        <b>Total:</b>

                        RM {{ "%.2f"|format(order.total) }}

                    </p>


                    <form
                        method="POST"
                        action="/update_status/{{ loop.index0 }}"
                    >

                        <label>
                            Change Status:
                        </label>

                        <select name="status">

                            <option
                            value="Pending"
                            {% if order.status == "Pending" %}
                            selected
                            {% endif %}>
                                Pending
                            </option>

                            <option
                            value="Preparing"
                            {% if order.status == "Preparing" %}
                            selected
                            {% endif %}>
                                Preparing
                            </option>

                            <option
                            value="Ready"
                            {% if order.status == "Ready" %}
                            selected
                            {% endif %}>
                                Ready
                            </option>

                            <option
                            value="Completed"
                            {% if order.status == "Completed" %}
                            selected
                            {% endif %}>
                                Completed
                            </option>

                        </select>

                        <button type="submit">
                            Update Status
                        </button>

                    </form>


                    <p>

                        <a
                        class="delete"
                        href="/delete/{{ loop.index0 }}"
                        onclick="return confirm('Delete this order?');">

                            Delete Order

                        </a>

                    </p>

                </div>

                {% endfor %}

            {% else %}

                <p>No orders available.</p>

            {% endif %}

        </div>


        <div class="box">

            <h2>Testing</h2>

            <p>
                Use the button below to create sample orders
                for testing the system.
            </p>

            <form method="POST" action="/testing">

                <button type="submit">
                    Create Test Orders
                </button>

            </form>

        </div>

    </div>

    </body>

    </html>
    """

    # ==========================================
    # CALCULATE SUMMARY
    # ==========================================

    total_orders = len(orders)

    total_sales = 0

    pending = 0
    preparing = 0
    ready = 0
    completed = 0

    for order in orders:

        total_sales += order.get("total", 0)

        status = order.get("status", "Pending")

        if status == "Pending":
            pending += 1

        elif status == "Preparing":
            preparing += 1

        elif status == "Ready":
            ready += 1

        elif status == "Completed":
            completed += 1


    # ==========================================
    # SIMPLE TEMPLATE REPLACEMENT
    # ==========================================

    from jinja2 import Template

    template = Template(html)

    return template.render(
        orders=orders,
        search_result=search_result,
        search_type=search_type,
        search_value=search_value,
        total_orders=total_orders,
        total_sales=total_sales,
        pending=pending,
        preparing=preparing,
        ready=ready,
        completed=completed
    )


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    orders = load_orders()

    orders = prepare_orders(orders)

    orders = update_automatic_status(orders)

    return create_page(orders)


# ==========================================
# SEARCH ORDERS
# ==========================================

@app.route("/search", methods=["POST"])
def search_order():

    orders = load_orders()

    orders = prepare_orders(orders)

    orders = update_automatic_status(orders)

    search = request.form["search"].strip()

    search_type = request.form["search_type"]

    search_result = []


    # ------------------------------------------
    # SEARCH BY FOOD NAME
    # ------------------------------------------

    if search_type == "food":

        search = search.lower()

        for order in orders:

            for item in order["items"]:

                if search in item["name"].lower():

                    search_result.append(order)

                    break


    # ------------------------------------------
    # SEARCH BY TABLE NUMBER
    # ------------------------------------------

    elif search_type == "table":

        for order in orders:

            if str(order["table_number"]) == search:

                search_result.append(order)


    # ------------------------------------------
    # SEARCH BY STATUS
    # ------------------------------------------

    elif search_type == "status":

        search = search.lower()

        for order in orders:

            if order["status"].lower() == search:

                search_result.append(order)


    return create_page(
        orders,
        search_result,
        search_type,
        search
    )


# ==========================================
# UPDATE ORDER STATUS
# ==========================================

@app.route(
    "/update_status/<int:order_number>",
    methods=["POST"]
)
def update_status(order_number):

    orders = load_orders()

    orders = prepare_orders(orders)

    if order_number >= 0 and order_number < len(orders):

        new_status = request.form["status"]

        valid_statuses = [
            "Pending",
            "Preparing",
            "Ready",
            "Completed"
        ]

        if new_status in valid_statuses:

            orders[order_number]["status"] = new_status

            save_orders(orders)

    return redirect("/")


# ==========================================
# DELETE ORDER
# ==========================================

@app.route("/delete/<int:order_number>")
def delete_order(order_number):

    orders = load_orders()

    orders = prepare_orders(orders)

    if order_number >= 0 and order_number < len(orders):

        orders.pop(order_number)

        save_orders(orders)

    return redirect("/")


# ==========================================
# TESTING FUNCTION
# ==========================================

@app.route("/testing", methods=["POST"])
def create_test_orders():

    orders = load_orders()

    orders = prepare_orders(orders)


    # ------------------------------------------
    # TEST ORDER 1
    # ------------------------------------------

    test_order_1 = {

        "table_number": 1,

        "items": [

            {
                "name": "Chicken Rice",
                "price": 6.00,
                "quantity": 2
            },

            {
                "name": "Iced Milo",
                "price": 2.50,
                "quantity": 1
            }

        ],

        "total": 14.50,

        "status": "Pending",

        "order_time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    }


    # ------------------------------------------
    # TEST ORDER 2
    # ------------------------------------------

    test_order_2 = {

        "table_number": 2,

        "items": [

            {
                "name": "Nasi Lemak",
                "price": 5.00,
                "quantity": 1
            },

            {
                "name": "Mineral Water",
                "price": 1.50,
                "quantity": 2
            }

        ],

        "total": 8.00,

        "status": "Preparing",

        "order_time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    }


    # ------------------------------------------
    # TEST ORDER 3
    # ------------------------------------------

    test_order_3 = {

        "table_number": 3,

        "items": [

            {
                "name": "Fried Noodles",
                "price": 5.50,
                "quantity": 1
            },

            {
                "name": "Iced Milo",
                "price": 2.50,
                "quantity": 2
            }

        ],

        "total": 10.50,

        "status": "Ready",

        "order_time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    }


    orders.append(test_order_1)

    orders.append(test_order_2)

    orders.append(test_order_3)

    save_orders(orders)

    return redirect("/")


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    webbrowser.open(
        "http://127.0.0.1:5000"
    )

    app.run(debug=True)