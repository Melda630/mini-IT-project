from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# -----------------------------
# FOOD MENU
# -----------------------------

food_menu = [
    {
        "id": 1,
        "name": "Chicken Rice",
        "category": "Main Meal",
        "price": 6.00
    },
    {
        "id": 2,
        "name": "Nasi Lemak",
        "category": "Main Meal",
        "price": 5.00
    },
    {
        "id": 3,
        "name": "Fried Noodles",
        "category": "Main Meal",
        "price": 5.50
    },
    {
        "id": 4,
        "name": "Iced Milo",
        "category": "Beverage",
        "price": 2.50
    },
    {
        "id": 5,
        "name": "Mineral Water",
        "category": "Beverage",
        "price": 1.50
    }
]


# -----------------------------
# MAIN MENU
# -----------------------------

@app.route("/")
def main_menu():
    return render_template(
        "index.html",
        food_menu=food_menu
    )


# -----------------------------
# VIEW FOOD MENU
# -----------------------------

@app.route("/food-menu")
def view_food_menu():
    return render_template(
        "food_menu.html",
        food_menu=food_menu
    )


# -----------------------------
# USER INTERACTION
# -----------------------------

@app.route("/order", methods=["GET", "POST"])
def order():

    message = ""

    if request.method == "POST":

        customer_name = request.form.get("customer_name")
        food_id = request.form.get("food_id")
        quantity = request.form.get("quantity")

        # Check customer name
        if customer_name == "":
            message = "Please enter your name."

        # Check food selection
        elif food_id == "":
            message = "Please select a food item."

        # Check quantity
        elif quantity == "":
            message = "Please enter quantity."

        else:
            message = (
                "Order received! "
                + customer_name
                + " selected food item "
                + food_id
                + " with quantity "
                + quantity
                + "."
            )

    return render_template(
        "order.html",
        food_menu=food_menu,
        message=message
    )


# -----------------------------
# RUN APPLICATION
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)