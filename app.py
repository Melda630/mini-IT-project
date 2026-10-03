from flask import Flask, render_template, request, redirect, url_for, session, flash

from ordering import (
    cart,
    order_history,
    add_to_cart,
    calculate_total,
    modify_quantity,
    remove_item,
    checkout
)
from order_history import (
    add_history,
    get_current_table_orders,
    search_by_order_id,
    search_by_date,
    get_daily_summary,
    calculate_table_total,
    update_history,
    delete_history
)
from menu_operations import (
    get_all_items,
    filter_menu_items,
    add_menu_item,
    update_menu_item_by_id,
    delete_menu_item_by_id
)


app = Flask(__name__)

app.secret_key = "campus-food-secret-key"

ADMIN_ID = "admin"
ADMIN_PASSWORD = "1234"

menu = [
    {"name": "Chicken Rice", "price": 6.00},
    {"name": "Nasi Lemak", "price": 5.00},
    {"name": "Fried Noodles", "price": 5.50},
    {"name": "Iced Milo", "price": 2.50},
    {"name": "Mineral Water", "price": 1.50}
]


# Customer homepage
@app.route("/")
def home():
    if "user_type" not in session:
        session["user_type"] = "guest"

    return redirect(url_for("food_menu"))


# Admin login
@app.route("/admin-login")
def admin_login_page():
    return render_template("login.html")


@app.route("/admin-login-submit", methods=["POST"])
def admin_login():
    admin_id = request.form["admin_id"]
    password = request.form["password"]

    if admin_id == ADMIN_ID and password == ADMIN_PASSWORD:
        session["user_type"] = "admin"
        return redirect(url_for("admin_dashboard"))

    return render_template(
        "login.html",
        error="Invalid admin ID or password"
    )


# Admin dashboard
@app.route("/admin")
def admin_dashboard():
    if session.get("user_type") != "admin":
        return redirect(url_for("admin_login_page"))

    selected_date = request.args.get("date")
    order_id = request.args.get("order_id")

    summary = get_daily_summary()
    orders = []
    selected_order = None

    if selected_date:
        orders = search_by_date(selected_date)

    if order_id and selected_date:
        results = search_by_order_id(
            order_id,
            selected_date
        )

        if results:
            selected_order = results[0]

    return render_template(
        "admin.html",
        menu=menu,
        summary=summary,
        orders=orders,
        selected_date=selected_date,
        selected_order=selected_order
    )


@app.route("/admin/complete", methods=["POST"])
def complete_order():
    order_id = request.form.get("order_id")
    order_date = request.form.get("date")

    update_history(order_id, order_date, "Completed")

    return redirect(
        url_for(
            "admin_dashboard",
            order_id=order_id,
            date=order_date
        )
    )


@app.route("/admin/delete", methods=["POST"])
def delete_order():
    order_id = request.form.get("order_id")
    order_date = request.form.get("date")

    delete_history(order_id, order_date)

    return redirect(
        url_for(
            "admin_dashboard",
            date=order_date
        )
    )


# Admin logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# Add food to cart
@app.route("/add", methods=["POST"])
def add_item():
    item_name = request.form["item_name"]
    price = float(request.form["price"])

    try:
        quantity = int(request.form["quantity"])
    except ValueError:
        quantity = 0

    add_to_cart(item_name, price, quantity)

    return redirect(url_for("food_menu"))


# View cart
@app.route("/cart")
def view_cart():
    return render_template(
        "cart.html",
        cart=cart,
        total=calculate_total()
    )


# Update item quantity
@app.route("/modify", methods=["POST"])
def modify_item():
    try:
        item_number = int(request.form["item_number"])
        quantity = int(request.form["quantity"])

        modify_quantity(item_number, quantity)

    except ValueError:
        pass

    return redirect(url_for("view_cart"))


# Remove item from cart
@app.route("/remove/<int:item_number>")
def remove(item_number):
    remove_item(item_number)

    return redirect(url_for("view_cart"))


# Checkout order
@app.route("/checkout", methods=["POST"])
def checkout_order():
    order_type = request.form.get("order_type")
    table_number = request.form.get("table_number")

    if order_type not in ["Dine In", "Pickup"]:
        return redirect(url_for("view_cart"))

    if order_type == "Dine In" and not table_number:
        return redirect(url_for("view_cart"))

    if order_type == "Pickup":
        table_number = None

    success = checkout(order_type)

    if success:
        completed_order = order_history[-1]

        saved_order = add_history(
            table_number,
            completed_order
        )

        if order_type == "Dine In":
            return redirect(
                url_for(
                    "my_orders",
                    table_number=table_number
                )
            )

        return redirect(
            url_for(
                "my_orders",
                order_id=saved_order["order_id"]
            )
        )

    return redirect(url_for("view_cart"))


# Customer's current orders
@app.route("/my-orders")
def my_orders():
    table_number = request.args.get("table_number")
    order_id = request.args.get("order_id")

    orders = []
    table_total = 0
    takeaway_order = None

    if table_number:
        orders = get_current_table_orders(table_number)
        table_total = calculate_table_total(orders)

    if order_id:
        results = search_by_order_id(order_id)

        if results:
            takeaway_order = results[-1]

    return render_template(
        "my_order.html",
        table_number=table_number,
        orders=orders,
        table_total=table_total,
        takeaway_order=takeaway_order
    )


# Order history (goes to customer's orders page)
@app.route("/history")
def history():
    return redirect(url_for("my_orders"))


# Food menu
@app.route("/food_menu", methods=["GET"])
def food_menu():
    search_query = request.args.get("search", "").strip()
    category_filter = request.args.get("category", "").strip()

    filtered_items = filter_menu_items(
        category_filter=category_filter,
        search_query=search_query
    )

    cart_count = sum(item["quantity"] for item in cart)
    cart_total = calculate_total()

    return render_template(
        "food_menu.html",
        items=filtered_items,
        cart_count=cart_count,
        cart_total=cart_total
    )


# Add and view menu items
@app.route("/menu_crud", methods=["GET", "POST"])
def menu_crud():
    if request.method == "POST":
        item_name = request.form.get("name", "")
        item_category = request.form.get("category", "")
        item_price = request.form.get("price", "0")

        if not item_name.strip():
            flash("Error: Item name cannot be empty.")
            return redirect(url_for("menu_crud"))

        if not item_category.strip():
            flash("Error: Please select a category.")
            return redirect(url_for("menu_crud"))

        try:
            price_val = float(item_price)

            if price_val <= 0:
                flash("Error: Price must be a positive number greater than 0.")
                return redirect(url_for("menu_crud"))

        except ValueError:
            flash("Error: Invalid price format. Please enter a valid number.")
            return redirect(url_for("menu_crud"))

        success, message = add_menu_item(
            item_name,
            item_category,
            item_price
        )

        flash(message)

        return redirect(url_for("menu_crud"))

    items = get_all_items()

    return render_template(
        "menu_crud.html",
        items=items
    )


# Update menu item
@app.route("/update_menu_item/<int:item_id>", methods=["POST"])
def update_menu_item(item_id):
    item_name = request.form.get("name", "")
    item_category = request.form.get("category", "")
    item_price = request.form.get("price", "0")

    if not item_name.strip():
        flash("Error: Item name cannot be empty.")
        return redirect(url_for("menu_crud"))

    try:
        price_val = float(item_price)

        if price_val <= 0:
            flash("Error: Price must be greater than 0.")
            return redirect(url_for("menu_crud"))

    except ValueError:
        flash("Error: Invalid price format.")
        return redirect(url_for("menu_crud"))

    success, message = update_menu_item_by_id(
        item_id,
        item_name,
        item_category,
        item_price
    )

    flash(message)

    return redirect(url_for("menu_crud"))


# Delete menu item
@app.route("/delete_menu_item/<int:item_id>")
def delete_menu_item(item_id):
    success, message = delete_menu_item_by_id(item_id)

    flash(message)

    return redirect(url_for("menu_crud"))


# Customer feedback
@app.route("/user_interaction", methods=["GET", "POST"])
def user_interaction():
    if request.method == "POST":
        feedback_text = request.form.get(
            "feedback",
            ""
        ).strip()

        if feedback_text:
            flash(
                "Thank you! Your feedback/query has been submitted successfully."
            )
        else:
            flash("Please enter a message before submitting.")

        return redirect(url_for("user_interaction"))

    return render_template("user_interaction.html")


# Run the website
if __name__ == "__main__":
    import webbrowser
    from threading import Timer

    Timer(
        1,
        lambda: webbrowser.open("http://127.0.0.1:5000")
    ).start()

    app.run(
        debug=True,
        use_reloader=False,
        port=5000
    )