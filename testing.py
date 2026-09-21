# ==========================================
# CAMPUS FOOD ORDERING SYSTEM
# MEMBER 3
# TESTING
# ==========================================

import json
from datetime import datetime, timedelta


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
# CREATE TEST ORDER
# ==========================================

def create_order(
    table_number,
    items,
    total,
    status,
    order_time
):

    return {

        "table_number": table_number,

        "items": items,

        "total": total,

        "status": status,

        "order_time": order_time,

        "manual_status": True

    }


# ==========================================
# CREATE MULTIPLE TEST ORDERS
# ==========================================

def create_test_orders():

    orders = []


    # ======================================
    # TABLE 1 - 2 ORDERS
    # ======================================

    orders.append(
        create_order(
            1,
            [
                {
                    "name": "Chicken Rice",
                    "quantity": 2,
                    "price": 6.00
                },
                {
                    "name": "Iced Milo",
                    "quantity": 1,
                    "price": 2.50
                }
            ],
            14.50,
            "Pending",
            "2026-09-21 08:30:00"
        )
    )


    orders.append(
        create_order(
            1,
            [
                {
                    "name": "Nasi Lemak",
                    "quantity": 1,
                    "price": 5.00
                },
                {
                    "name": "Mineral Water",
                    "quantity": 1,
                    "price": 1.50
                }
            ],
            6.50,
            "Preparing",
            "2026-09-21 08:45:00"
        )
    )


    # ======================================
    # TABLE 2 - 2 ORDERS
    # ======================================

    orders.append(
        create_order(
            2,
            [
                {
                    "name": "Fried Noodles",
                    "quantity": 1,
                    "price": 5.50
                },
                {
                    "name": "Iced Milo",
                    "quantity": 2,
                    "price": 2.50
                }
            ],
            10.50,
            "Ready",
            "2026-09-21 09:00:00"
        )
    )


    orders.append(
        create_order(
            2,
            [
                {
                    "name": "Chicken Rice",
                    "quantity": 1,
                    "price": 6.00
                },
                {
                    "name": "Mineral Water",
                    "quantity": 2,
                    "price": 1.50
                }
            ],
            9.00,
            "Completed",
            "2026-09-21 09:15:00"
        )
    )


    # ======================================
    # TABLE 3 - 2 ORDERS
    # ======================================

    orders.append(
        create_order(
            3,
            [
                {
                    "name": "Nasi Lemak",
                    "quantity": 2,
                    "price": 5.00
                }
            ],
            10.00,
            "Pending",
            "2026-09-21 09:30:00"
        )
    )


    orders.append(
        create_order(
            3,
            [
                {
                    "name": "Fried Noodles",
                    "quantity": 2,
                    "price": 5.50
                },
                {
                    "name": "Mineral Water",
                    "quantity": 1,
                    "price": 1.50
                }
            ],
            12.50,
            "Preparing",
            "2026-09-21 09:45:00"
        )
    )


    # ======================================
    # TABLE 4 - 2 ORDERS
    # ======================================

    orders.append(
        create_order(
            4,
            [
                {
                    "name": "Chicken Rice",
                    "quantity": 1,
                    "price": 6.00
                },
                {
                    "name": "Iced Milo",
                    "quantity": 1,
                    "price": 2.50
                }
            ],
            8.50,
            "Ready",
            "2026-09-21 10:00:00"
        )
    )


    orders.append(
        create_order(
            4,
            [
                {
                    "name": "Nasi Lemak",
                    "quantity": 1,
                    "price": 5.00
                },
                {
                    "name": "Iced Milo",
                    "quantity": 1,
                    "price": 2.50
                },
                {
                    "name": "Mineral Water",
                    "quantity": 1,
                    "price": 1.50
                }
            ],
            9.00,
            "Completed",
            "2026-09-21 10:15:00"
        )
    )


    # ======================================
    # TABLE 5 - 2 ORDERS
    # ======================================

    orders.append(
        create_order(
            5,
            [
                {
                    "name": "Fried Noodles",
                    "quantity": 1,
                    "price": 5.50
                }
            ],
            5.50,
            "Pending",
            "2026-09-21 10:30:00"
        )
    )


    orders.append(
        create_order(
            5,
            [
                {
                    "name": "Chicken Rice",
                    "quantity": 2,
                    "price": 6.00
                }
            ],
            12.00,
            "Preparing",
            "2026-09-21 10:45:00"
        )
    )


    # ======================================
    # TABLE 6 - 3 ORDERS
    # ======================================

    orders.append(
        create_order(
            6,
            [
                {
                    "name": "Nasi Lemak",
                    "quantity": 2,
                    "price": 5.00
                }
            ],
            10.00,
            "Ready",
            "2026-09-21 11:00:00"
        )
    )


    orders.append(
        create_order(
            6,
            [
                {
                    "name": "Chicken Rice",
                    "quantity": 1,
                    "price": 6.00
                },
                {
                    "name": "Mineral Water",
                    "quantity": 1,
                    "price": 1.50
                }
            ],
            7.50,
            "Completed",
            "2026-09-21 11:15:00"
        )
    )


    orders.append(
        create_order(
            6,
            [
                {
                    "name": "Iced Milo",
                    "quantity": 2,
                    "price": 2.50
                }
            ],
            5.00,
            "Pending",
            "2026-09-21 11:30:00"
        )
    )


    # ======================================
    # TABLE 7 - 3 ORDERS
    # ======================================

    orders.append(
        create_order(
            7,
            [
                {
                    "name": "Fried Noodles",
                    "quantity": 2,
                    "price": 5.50
                }
            ],
            11.00,
            "Preparing",
            "2026-09-21 11:45:00"
        )
    )


    orders.append(
        create_order(
            7,
            [
                {
                    "name": "Chicken Rice",
                    "quantity": 1,
                    "price": 6.00
                },
                {
                    "name": "Iced Milo",
                    "quantity": 1,
                    "price": 2.50
                }
            ],
            8.50,
            "Ready",
            "2026-09-21 12:00:00"
        )
    )


    orders.append(
        create_order(
            7,
            [
                {
                    "name": "Nasi Lemak",
                    "quantity": 1,
                    "price": 5.00
                },
                {
                    "name": "Mineral Water",
                    "quantity": 1,
                    "price": 1.50
                }
            ],
            6.50,
            "Completed",
            "2026-09-21 12:15:00"
        )
    )


    # Save all test orders

    save_orders(orders)

    return orders


# ==========================================
# TEST FOOD SEARCH
# ==========================================

def test_food_search(orders):

    print("\n==========================================")
    print("TEST 1: SEARCH BY FOOD NAME")
    print("==========================================")

    search_food = "Chicken Rice"

    results = []

    for order in orders:

        for item in order.get("items", []):

            if search_food.lower() in item.get(
                "name", ""
            ).lower():

                results.append(order)

                break


    print("Searching for:", search_food)

    print("Orders found:", len(results))

    if len(results) > 0:
        print("RESULT: PASS")
    else:
        print("RESULT: FAIL")


# ==========================================
# TEST TABLE SEARCH
# ==========================================

def test_table_search(orders):

    print("\n==========================================")
    print("TEST 2: SEARCH BY TABLE NUMBER")
    print("==========================================")

    search_table = "3"

    results = []

    for order in orders:

        table_number = str(
            order.get(
                "table_number",
                ""
            )
        )

        if table_number == search_table:

            results.append(order)


    print("Searching for Table:", search_table)

    print("Orders found:", len(results))

    if len(results) == 2:
        print("RESULT: PASS")
    else:
        print("RESULT: FAIL")


# ==========================================
# TEST STATUS SEARCH
# ==========================================

def test_status_search(orders):

    print("\n==========================================")
    print("TEST 3: SEARCH BY ORDER STATUS")
    print("==========================================")

    search_status = "Completed"

    results = []

    for order in orders:

        if order.get(
            "status",
            ""
        ) == search_status:

            results.append(order)


    print("Searching for Status:", search_status)

    print("Orders found:", len(results))

    if len(results) > 0:
        print("RESULT: PASS")
    else:
        print("RESULT: FAIL")


# ==========================================
# TEST MULTIPLE ORDERS PER TABLE
# ==========================================

def test_multiple_orders(orders):

    print("\n==========================================")
    print("TEST 4: MULTIPLE ORDERS PER TABLE")
    print("==========================================")

    table_counts = {}

    for order in orders:

        table = order.get(
            "table_number",
            0
        )

        if table not in table_counts:

            table_counts[table] = 0

        table_counts[table] += 1


    print("\nOrders by table:")

    for table in sorted(table_counts):

        print(
            "Table",
            table,
            ":",
            table_counts[table],
            "orders"
        )


    if (
        table_counts.get(1) == 2
        and table_counts.get(2) == 2
        and table_counts.get(3) == 2
        and table_counts.get(4) == 2
        and table_counts.get(5) == 2
        and table_counts.get(6) == 3
        and table_counts.get(7) == 3
    ):

        print("\nRESULT: PASS")

    else:

        print("\nRESULT: FAIL")


# ==========================================
# TEST ORDER STATUS
# ==========================================

def test_order_status(orders):

    print("\n==========================================")
    print("TEST 5: ORDER STATUS")
    print("==========================================")

    valid_statuses = [

        "Pending",
        "Preparing",
        "Ready",
        "Completed"

    ]

    passed = True

    for order in orders:

        status = order.get(
            "status",
            ""
        )

        if status not in valid_statuses:

            passed = False


    if passed:

        print("All orders have valid statuses.")

        print("RESULT: PASS")

    else:

        print("Invalid status found.")

        print("RESULT: FAIL")


# ==========================================
# TEST DATA STORAGE
# ==========================================

def test_data_storage():

    print("\n==========================================")
    print("TEST 6: DATA STORAGE")
    print("==========================================")

    orders = load_orders()

    print(
        "Orders loaded from JSON:",
        len(orders)
    )

    if len(orders) == 16:

        print("RESULT: PASS")

    else:

        print("RESULT: FAIL")


# ==========================================
# TEST SUMMARY
# ==========================================

def test_summary(orders):

    print("\n==========================================")
    print("TEST 7: ORDER SUMMARY")
    print("==========================================")

    total_orders = len(orders)

    total_sales = 0

    for order in orders:

        total_sales += float(
            order.get(
                "total",
                0
            )
        )


    print("Total Orders:", total_orders)

    print(
        "Total Sales: RM",
        format(total_sales, ".2f")
    )

    if total_orders == 16:

        print("RESULT: PASS")

    else:

        print("RESULT: FAIL")


# ==========================================
# RUN ALL TESTS
# ==========================================

if __name__ == "__main__":

    print("\n")
    print("==========================================")
    print("CAMPUS FOOD ORDERING SYSTEM")
    print("MEMBER 3 TESTING")
    print("==========================================")


    # Create fresh test data

    orders = create_test_orders()


    print("\nTest data created successfully.")

    print(
        "Total test orders:",
        len(orders)
    )


    # Run tests

    test_food_search(orders)

    test_table_search(orders)

    test_status_search(orders)

    test_multiple_orders(orders)

    test_order_status(orders)

    test_data_storage()

    test_summary(orders)


    print("\n==========================================")
    print("ALL TESTING COMPLETED")
    print("==========================================")