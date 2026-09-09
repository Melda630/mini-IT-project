from flask import Flask, render_template, request, redirect, url_for

from ordering import (
    cart,
    order_history,
    add_to_cart,
    calculate_total,
    modify_quantity,
    remove_item,
    checkout
)


app = Flask(__name__)


menu = [
    {"name": "Chicken Rice", "price": 6.00},
    {"name": "Nasi Lemak", "price": 5.00},
    {"name": "Fried Noodles", "price": 5.50},
    {"name": "Iced Milo", "price": 2.50},
    {"name": "Mineral Water", "price": 1.50}
]


@app.route("/")
def home():
    return render_template(
        "index.html",
        menu=menu
    )


@app.route("/add", methods=["POST"])
def add_item():
    item_name = request.form["item_name"]
    price = float(request.form["price"])

    try:
        quantity = int(request.form["quantity"])
    except ValueError:
        quantity = 0

    add_to_cart(
        item_name,
        price,
        quantity
    )

    return redirect(url_for("home"))


@app.route("/cart")
def view_cart():
    return render_template(
        "cart.html",
        cart=cart,
        total=calculate_total()
    )


@app.route("/modify", methods=["POST"])
def modify_item():
    try:
        item_number = int(request.form["item_number"])
        quantity = int(request.form["quantity"])

        modify_quantity(
            item_number,
            quantity
        )

    except ValueError:
        pass

    return redirect(url_for("view_cart"))


@app.route("/remove/<int:item_number>")
def remove(item_number):
    remove_item(item_number)

    return redirect(url_for("view_cart"))


@app.route("/checkout", methods=["POST"])
def checkout_order():
    success = checkout()

    if success:
        return redirect(url_for("history"))

    return redirect(url_for("view_cart"))


@app.route("/history")
def history():
    return render_template(
        "history.html",
        order_history=order_history
    )


if __name__ == "__main__":
    import webbrowser
    from threading import Timer

    Timer(1, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=True, use_reloader=False)