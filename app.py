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

from menu_operations import (
    get_all_items,
    filter_menu_items,
    add_menu_item,
    update_menu_item_by_id,
    delete_menu_item_by_id
)


app = Flask(__name__)
app.secret_key = "campus_food_ordering_system_secret_key"

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

    cart_count = sum(item["quantity"] for item in cart)
    cart_total = calculate_total()

    return render_template(
        "index.html",
        menu=menu,
        cart_count=cart_count,
        cart_total=cart_total
    )


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

    return render_template(
        "admin.html",
        menu=menu,
        order_history=order_history
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

    if order_type not in ["Dine In", "Pickup"]:
        return redirect(url_for("view_cart"))

    success = checkout(order_type)

    if success:
        return redirect(url_for("history"))

    return redirect(url_for("view_cart"))


# View previous orders
@app.route("/history")
def history():
    return render_template(
        "history.html",
        order_history=order_history
    )


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