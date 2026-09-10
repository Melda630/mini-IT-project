# ==========================================
# CAMPUS FOOD ORDERING SYSTEM
# MEMBER 3
# Order History, Search, Data Storage & Testing
# ==========================================

from flask import Flask, request, redirect
import json

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
# HTML FRONTEND
# ==========================================

def create_page(orders, search_result=None):

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
                padding: 30px;
            }

            .container {
                width: 80%;
                margin: auto;
                background-color: white;
                padding: 25px;
                border-radius: 10px;
            }

            h1 {
                text-align: center;
            }

            h2 {
                border-bottom: 1px solid #ccc;
                padding-bottom: 10px;
            }

            input {
                padding: 10px;
                width: 60%;
            }

            button {
                padding: 10px 20px;
                cursor: pointer;
            }

            .order {
                border: 1px solid #ccc;
                padding: 15px;
                margin-top: 15px;
                border-radius: 5px;
            }

            .delete {
                color: red;
            }

            .summary {
                background-color: #eeeeee;
                padding: 15px;
                margin-top: 20px;
            }

        </style>

    </head>


    <body>

        <div class="container">

            <h1>Campus Food Ordering System</h1>

            <h2>Order History</h2>

            <form action="/search" method="POST">

                <input
                    type="text"
                    name="search"
                    placeholder="Search food name"
                    required
                >

                <button type="submit">Search</button>

            </form>

    """

    # ==========================================
    # SEARCH RESULTS
    # ==========================================

    if search_result is not None:

        html += "<h2>Search Results</h2>"

        if len(search_result) == 0:

            html += "<p>No matching order found.</p>"

        else:

            for order_number, order in enumerate(search_result, start=1):

                html += "<div class='order'>"

                html += f"<h3>Order {order_number}</h3>"

                for item in order["items"]:

                    subtotal = item["price"] * item["quantity"]

                    html += f"""
                    <p>
                        {item["name"]}
                        x {item["quantity"]}
                        - RM{subtotal:.2f}
                    </p>
                    """

                html += f"""
                    <strong>
                        Total: RM{order["total"]:.2f}
                    </strong>
                """

                html += "</div>"

        html += "<br>"
        html += "<a href='/'>Show All Orders</a>"


    # ==========================================
    # DISPLAY ALL ORDERS
    # ==========================================

    html += "<h2>All Previous Orders</h2>"

    if len(orders) == 0:

        html += "<p>No order history available.</p>"

    else:

        for number, order in enumerate(orders, start=1):

            html += "<div class='order'>"

            html += f"<h3>Order {number}</h3>"

            for item in order["items"]:

                subtotal = item["price"] * item["quantity"]

                html += f"""
                <p>
                    {item["name"]}
                    x {item["quantity"]}
                    - RM{subtotal:.2f}
                </p>
                """

            html += f"""
                <p>
                    <strong>
                        Total: RM{order["total"]:.2f}
                    </strong>
                </p>

                <a class="delete"
                   href="/delete/{number - 1}"
                   onclick="return confirm('Delete this order?')">

                   Delete Order

                </a>
            """

            html += "</div>"


    # ==========================================
    # ORDER SUMMARY
    # ==========================================

    total_orders = len(orders)

    total_spending = 0

    for order in orders:

        total_spending += order["total"]


    html += f"""
        <div class="summary">

            <h3>Order Summary</h3>

            <p>Total Orders: {total_orders}</p>

            <p>
                Total Spending:
                RM{total_spending:.2f}
            </p>

        </div>

        </div>

    </body>

    </html>
    """

    return html


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    orders = load_orders()

    return create_page(orders)


# ==========================================
# SEARCH ORDER
# ==========================================

@app.route("/search", methods=["POST"])
def search_order():

    orders = load_orders()

    search = request.form["search"].lower()

    search_result = []

    for order in orders:

        for item in order["items"]:

            if search in item["name"].lower():

                search_result.append(order)

                break

    return create_page(orders, search_result)


# ==========================================
# DELETE ORDER
# ==========================================

@app.route("/delete/<int:order_number>")
def delete_order(order_number):

    orders = load_orders()

    if order_number >= 0 and order_number < len(orders):

        orders.pop(order_number)

        save_orders(orders)

    return redirect("/")




# ==========================================
# START PROGRAM
# ==========================================



if __name__ == "__main__":

    app.run(debug=True)