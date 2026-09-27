from flask import Flask, render_template, request, redirect, url_for, flash
from menu_operations import (
    get_all_items,
    filter_menu_items,
    add_menu_item,
    update_menu_item_by_id,
    delete_menu_item_by_id
)

app = Flask(__name__)
app.secret_key = "campus_food_ordering_system_secret_key"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/food_menu", methods=["GET"])
def food_menu():
    search_query = request.args.get("search", "").strip()
    category_filter = request.args.get("category", "").strip()

    filtered_items = filter_menu_items(
        category_filter=category_filter,
        search_query=search_query
    )

    return render_template("food_menu.html", items=filtered_items)


@app.route("/menu_crud", methods=["GET", "POST"])
def menu_crud():
    if request.method == "POST":
        item_name = request.form.get("name", "")
        item_category = request.form.get("category", "")
        item_price = request.form.get("price", "0")

        # Basic Input Validation Checks
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

        # Add item if validation passes
        success, message = add_menu_item(item_name, item_category, item_price)
        flash(message)

        return redirect(url_for("menu_crud"))

    items = get_all_items()
    return render_template("menu_crud.html", items=items)


@app.route("/update_menu_item/<int:item_id>", methods=["POST"])
def update_menu_item(item_id):
    item_name = request.form.get("name", "")
    item_category = request.form.get("category", "")
    item_price = request.form.get("price", "0")

    # Input Validation for Update
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

    success, message = update_menu_item_by_id(item_id, item_name, item_category, item_price)
    flash(message)
    return redirect(url_for("menu_crud"))


@app.route("/delete_menu_item/<int:item_id>")
def delete_menu_item(item_id):
    success, message = delete_menu_item_by_id(item_id)
    flash(message)
    return redirect(url_for("menu_crud"))


@app.route("/user_interaction", methods=["GET", "POST"])
def user_interaction():
    if request.method == "POST":
        feedback_text = request.form.get("feedback", "").strip()
        if feedback_text:
            flash("Thank you! Your feedback/query has been submitted successfully.")
        else:
            flash("Please enter a message before submitting.")
        return redirect(url_for("user_interaction"))

    return render_template("user_interaction.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)