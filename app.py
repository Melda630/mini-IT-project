# ==========================================
# CAMPUS FOOD ORDERING SYSTEM
# MEMBER 3
# Order History, Search, Data Storage
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
        with open(FILE_NAME, "r") as file:
            orders = json.load(file)

        if isinstance(orders, list):
            return orders

        return []

    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_orders(orders):
    with open(FILE_NAME, "w") as file:
        json.dump(orders, file, indent=4)


# ==========================================
# PREPARE ORDERS
# ==========================================

def prepare_orders(orders):

    changed = False

    for number, order in enumerate(orders):

        # Make sure items exists
        if "items" not in order:
            order["items"] = []
            changed = True

        # Add table number to older orders
        if "table_number" not in order:
            order["table_number"] = (number % 5) + 1
            changed = True

        # Add status to older orders
        if "status" not in order:
            order["status"] = "Pending"
            changed = True

        # Add order time to older orders
        if "order_time" not in order:
            order["order_time"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            changed = True

        # Add manual status flag
        if "manual_status" not in order:
            order["manual_status"] = False
            changed = True

    if changed:
        save_orders(orders)

    return orders


# ==========================================
# AUTOMATIC STATUS UPDATE
# ==========================================

def update_automatic_status(orders):

    changed = False

    for order in orders:

        # Do not automatically change a status
        # that was manually selected by staff
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

            # Automatic status system
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
# CREATE HTML PAGE
# ==========================================

def create_page(
    orders,
    search_result=None,
    search_type="food",
    search_value=""
):

    # ======================================
    # SUMMARY
    # ======================================

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
            total_sales += 0

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


    # ======================================
    # HTML
    # ======================================

    html = """
<!DOCTYPE html>

<html>

<head>

    <title>Campus Food Ordering System</title>

    <style>

        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            margin: 0;
            padding: 20px;
        }

        .container {
            max-width: 1000px;
            margin: auto;
        }

        h1 {
            text-align: center;
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
            background-color: #eeeeee;
            padding: 15px;
            border-radius: 8px;
            flex: 1;
            min-width: 120px;
            text-align: center;
        }

        input,
        select,
        button {
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

        .item {
            margin-left: 20px;
        }

        .status {
            font-weight: bold;
        }

        .delete {
            color: red;
            text-decoration: none;
        }

        .search-help {
            background-color: #eeeeee;
            padding: 10px;
            border-radius: 6px;
            margin-bottom: 10px;
        }

    </style>

</head>


<body>

<div class="container">


    <h1>Campus Food Ordering System</h1>


    <!-- =================================
         ORDER SUMMARY
         ================================= -->

    <div class="box">

        <h2>Order Summary</h2>

        <div class="summary">

            <div class="summary-box">

                <h3>{{ total_orders }}</h3>

                <p>Total Orders</p>

            </div>


            <div class="summary-box">

                <h3>
                    RM {{ "%.2f"|format(total_sales) }}
                </h3>

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


    <!-- =================================
         SEARCH ORDERS
         ================================= -->

    <div class="box">

        <h2>Search Orders</h2>


        <!-- STEP 1: CHOOSE SEARCH TYPE -->

        <form method="POST" action="/select_search">

            <label>

                <b>Search By:</b>

            </label>


            <select name="search_type">

                <option value="food"
                {% if search_type == "food" %}
                selected
                {% endif %}>

                    Food Name

                </option>


                <option value="table"
                {% if search_type == "table" %}
                selected
                {% endif %}>

                    Table Number

                </option>


                <option value="status"
                {% if search_type == "status" %}
                selected
                {% endif %}>

                    Order Status

                </option>

            </select>


            <button type="submit">

                Select Search Type

            </button>

        </form>


        <hr>


        <!-- STEP 2: ENTER SEARCH VALUE -->

        {% if search_type == "food" %}

        <div class="search-help">

            Search for an order using the food name.

        </div>


        <form method="POST" action="/search">

            <input
                type="hidden"
                name="search_type"
                value="food"
            >


            <input
                type="text"
                name="search"
                value="{{ search_value }}"
                placeholder="Enter food name..."
                required
            >


            <button type="submit">

                Search

            </button>

        </form>


        {% elif search_type == "table" %}

        <div class="search-help">

            Search for orders using the table number.

        </div>


        <form method="POST" action="/search">

            <input
                type="hidden"
                name="search_type"
                value="table"
            >


            <input
                type="number"
                name="search"
                value="{{ search_value }}"
                placeholder="Enter table number..."
                min="1"
                required
            >


            <button type="submit">

                Search

            </button>

        </form>


        {% elif search_type == "status" %}

        <div class="search-help">

            Select an order status to find matching orders.

        </div>


        <form method="POST" action="/search">

            <input
                type="hidden"
                name="search_type"
                value="status"
            >


            <select name="search">

                <option value="Pending"
                {% if search_value == "Pending" %}
                selected
                {% endif %}>

                    Pending

                </option>


                <option value="Preparing"
                {% if search_value == "Preparing" %}
                selected
                {% endif %}>

                    Preparing

                </option>


                <option value="Ready"
                {% if search_value == "Ready" %}
                selected
                {% endif %}>

                    Ready

                </option>


                <option value="Completed"
                {% if search_value == "Completed" %}
                selected
                {% endif %}>

                    Completed

                </option>

            </select>


            <button type="submit">

                Search

            </button>

        </form>

        {% endif %}

    </div>


    <!-- =================================
         SEARCH RESULTS
         ================================= -->

    {% if search_result is not none %}

    <div class="box">

        <h2>Search Results</h2>


        {% if search_result %}


            {% for order in search_result %}

            <div class="order">


                <h3>

                    Table {{ order["table_number"] }}

                </h3>


                <p>

                    <b>Status:</b>

                    <span class="status">

                        {{ order["status"] }}

                    </span>

                </p>


                <p>

                    <b>Order Time:</b>

                    {{ order["order_time"] }}

                </p>


                <p>

                    <b>Items:</b>

                </p>


                {% for item in order["items"] %}

                <p class="item">

                    {{ item["name"] }}

                    x {{ item["quantity"] }}

                    -

                    RM

                    {{ "%.2f"|format(
                        item["price"] * item["quantity"]
                    ) }}

                </p>

                {% endfor %}


                <p>

                    <b>Total:</b>

                    RM

                    {{ "%.2f"|format(
                        order["total"]
                    ) }}

                </p>


            </div>

            {% endfor %}


        {% else %}

            <p>

                No matching orders found.

            </p>

        {% endif %}

    </div>

    {% endif %}


    <!-- =================================
         ALL ORDERS
         ================================= -->

    <div class="box">

        <h2>All Order History</h2>


        {% if orders %}


            {% for order in orders %}

            <div class="order">


                <h3>

                    Table {{ order["table_number"] }}

                </h3>


                <p>

                    <b>Status:</b>

                    <span class="status">

                        {{ order["status"] }}

                    </span>

                </p>


                <p>

                    <b>Order Time:</b>

                    {{ order["order_time"] }}

                </p>


                <p>

                    <b>Items:</b>

                </p>


                {% for item in order["items"] %}

                <p class="item">

                    {{ item["name"] }}

                    x {{ item["quantity"] }}

                    -

                    RM

                    {{ "%.2f"|format(
                        item["price"] * item["quantity"]
                    ) }}

                </p>

                {% endfor %}


                <p>

                    <b>Total:</b>

                    RM

                    {{ "%.2f"|format(
                        order["total"]
                    ) }}

                </p>


                <!-- STATUS UPDATE -->

                <form
                    method="POST"
                    action="/update_status/{{ loop.index0 }}"
                >

                    <label>

                        <b>Change Status:</b>

                    </label>


                    <select name="status">

                        <option value="Pending"
                        {% if order["status"] == "Pending" %}
                        selected
                        {% endif %}>

                            Pending

                        </option>


                        <option value="Preparing"
                        {% if order["status"] == "Preparing" %}
                        selected
                        {% endif %}>

                            Preparing

                        </option>


                        <option value="Ready"
                        {% if order["status"] == "Ready" %}
                        selected
                        {% endif %}>

                            Ready

                        </option>


                        <option value="Completed"
                        {% if order["status"] == "Completed" %}
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
                    >

                        Delete Order

                    </a>

                </p>


            </div>

            {% endfor %}


        {% else %}

            <p>

                No orders available.

            </p>

        {% endif %}

    </div>


</div>

</body>

</html>
"""


    # ======================================
    # RENDER PAGE
    # ======================================

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

    return create_page(
        orders,
        search_result=None,
        search_type="food",
        search_value=""
    )


# ==========================================
# SELECT SEARCH TYPE
# ==========================================

@app.route("/select_search", methods=["POST"])
def select_search():

    orders = load_orders()

    orders = prepare_orders(orders)

    orders = update_automatic_status(orders)

    search_type = request.form.get(
        "search_type",
        "food"
    )

    # Show the correct search box
    # after the user chooses the search type.

    return create_page(
        orders,
        search_result=None,
        search_type=search_type,
        search_value=""
    )


# ==========================================
# SEARCH ORDERS
# ==========================================

@app.route("/search", methods=["POST"])
def search_order():

    orders = load_orders()

    orders = prepare_orders(orders)

    orders = update_automatic_status(orders)

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

        for order in orders:

            for item in order.get(
                "items",
                []
            ):

                item_name = str(
                    item.get("name", "")
                ).lower()

                if search_value_lower in item_name:

                    search_result.append(order)

                    break


    # ======================================
    # SEARCH BY TABLE
    # ======================================

    elif search_type == "table":

        for order in orders:

            table_number = str(
                order.get(
                    "table_number",
                    ""
                )
            )

            if table_number == search_value:

                search_result.append(order)


    # ======================================
    # SEARCH BY STATUS
    # ======================================

    elif search_type == "status":

        for order in orders:

            order_status = order.get(
                "status",
                "Pending"
            )

            if order_status == search_value:

                search_result.append(order)


    return create_page(

        orders,

        search_result,

        search_type,

        search_value

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

            # Save the selected status

            orders[order_number]["status"] = new_status

            # Tell the automatic system not to
            # overwrite the staff decision

            orders[order_number][
                "manual_status"
            ] = True

            save_orders(orders)


    return redirect("/")


# ==========================================
# DELETE ORDER
# ==========================================

@app.route(
    "/delete/<int:order_number>"
)
def delete_order(order_number):

    orders = load_orders()

    orders = prepare_orders(orders)


    if (
        order_number >= 0
        and order_number < len(orders)
    ):

        orders.pop(order_number)

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