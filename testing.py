# ==========================================
# TESTING FILE
# CAMPUS FOOD ORDERING SYSTEM
# MEMBER 3
# ==========================================

import json
from datetime import datetime, timedelta

FILE_NAME = "order_history.json"


# ==========================================
# CREATE FRESH TEST ORDERS
# ==========================================

def create_test_orders():

    current_time = datetime.now()

    orders = [

        {
            "table_number": 1,
            "items": [
                {
                    "name": "Chicken Rice",
                    "price": 6.00,
                    "quantity": 2
                }
            ],
            "total": 12.00
        },

        {
            "table_number": 2,
            "items": [
                {
                    "name": "Nasi Lemak",
                    "price": 5.00,
                    "quantity": 1
                },
                {
                    "name": "Iced Milo",
                    "price": 2.50,
                    "quantity": 1
                }
            ],
            "total": 7.50
        },

        {
            "table_number": 3,
            "items": [
                {
                    "name": "Fried Noodles",
                    "price": 5.50,
                    "quantity": 1
                },
                {
                    "name": "Mineral Water",
                    "price": 1.50,
                    "quantity": 2
                }
            ],
            "total": 8.50
        },

        {
            "table_number": 4,
            "items": [
                {
                    "name": "Chicken Rice",
                    "price": 6.00,
                    "quantity": 1
                },
                {
                    "name": "Iced Milo",
                    "price": 2.50,
                    "quantity": 2
                }
            ],
            "total": 11.00
        },

        {
            "table_number": 5,
            "items": [
                {
                    "name": "Nasi Lemak",
                    "price": 5.00,
                    "quantity": 2
                }
            ],
            "total": 10.00
        },

        {
            "table_number": 6,
            "items": [
                {
                    "name": "Fried Noodles",
                    "price": 5.50,
                    "quantity": 2
                },
                {
                    "name": "Mineral Water",
                    "price": 1.50,
                    "quantity": 1
                }
            ],
            "total": 12.50
        },

        {
            "table_number": 7,
            "items": [
                {
                    "name": "Chicken Rice",
                    "price": 6.00,
                    "quantity": 1
                },
                {
                    "name": "Nasi Lemak",
                    "price": 5.00,
                    "quantity": 1
                }
            ],
            "total": 11.00
        },

        {
            "table_number": 8,
            "items": [
                {
                    "name": "Iced Milo",
                    "price": 2.50,
                    "quantity": 2
                },
                {
                    "name": "Mineral Water",
                    "price": 1.50,
                    "quantity": 1
                }
            ],
            "total": 6.50
        },

        {
            "table_number": 9,
            "items": [
                {
                    "name": "Fried Noodles",
                    "price": 5.50,
                    "quantity": 1
                },
                {
                    "name": "Chicken Rice",
                    "price": 6.00,
                    "quantity": 1
                }
            ],
            "total": 11.50
        },

        {
            "table_number": 10,
            "items": [
                {
                    "name": "Nasi Lemak",
                    "price": 5.00,
                    "quantity": 1
                },
                {
                    "name": "Iced Milo",
                    "price": 2.50,
                    "quantity": 1
                },
                {
                    "name": "Mineral Water",
                    "price": 1.50,
                    "quantity": 1
                }
            ],
            "total": 9.00
        }

    ]


    # ======================================
    # ADD TIMESTAMP AND STATUS
    # ======================================

    for i, order in enumerate(orders):

        seconds_ago = (9 - i) * 20

        order_time = current_time - timedelta(
            seconds=seconds_ago
        )

        order["order_time"] = order_time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        order["status"] = "Pending"

        order["manual_status"] = False


    # ======================================
    # OVERWRITE OLD ORDER HISTORY
    # ======================================

    with open(FILE_NAME, "w") as file:

        json.dump(
            orders,
            file,
            indent=4
        )


    # ======================================
    # DISPLAY TEST RESULTS
    # ======================================

    print("==========================================")
    print("MULTIPLE ORDER TEST")
    print("==========================================")

    print()

    print("Old order history replaced.")

    print()

    print("Created 10 fresh test orders:")

    for order in orders:

        print(
            f"Table {order['table_number']} - "
            f"RM{order['total']:.2f} - "
            f"{order['order_time']}"
        )

    print()

    print("Total orders stored:", len(orders))

    print()

    print("Automatic status system:")

    print("0 - 29 seconds   = Pending")
    print("30 - 59 seconds  = Preparing")
    print("60 - 89 seconds  = Ready")
    print("90+ seconds      = Completed")

    print()

    print("==========================================")


# ==========================================
# RUN TEST
# ==========================================

if __name__ == "__main__":

    create_test_orders()