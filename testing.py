# ==========================================
# CAMPUS FOOD ORDERING SYSTEM
# MEMBER 3 - TESTING
# ==========================================

from app import load_orders, save_orders


def test_order_total():

    quantity = 2
    price = 6.00

    expected_total = 12.00
    actual_total = quantity * price

    print("\n--- TEST 1: ORDER TOTAL ---")

    print("Quantity:", quantity)
    print("Price: RM{:.2f}".format(price))
    print("Expected Total: RM{:.2f}".format(expected_total))
    print("Actual Total: RM{:.2f}".format(actual_total))

    if actual_total == expected_total:
        print("TEST PASSED!")
    else:
        print("TEST FAILED!")


def test_order_storage():

    print("\n--- TEST 2: ORDER STORAGE ---")

    # Create more than one order
    test_orders = [
        {
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
            "items": [
                {
                    "name": "Nasi Lemak",
                    "price": 5.00,
                    "quantity": 1
                }
            ],
            "total": 5.00
        },

        {
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
            "total": 10.50
        }
    ]

    save_orders(test_orders)

    loaded_orders = load_orders()

    print("Number of test orders:", len(loaded_orders))

    if loaded_orders == test_orders:
        print("TEST PASSED!")
    else:
        print("TEST FAILED!")


def test_search_order():

    print("\n--- TEST 3: SEARCH ORDER ---")

    orders = load_orders()

    # Search for Chicken Rice
    search = "Chicken Rice".lower()
    search_result = []

    for order in orders:
        for item in order["items"]:
            if search in item["name"].lower():
                search_result.append(order)
                break

    print("Searching for: Chicken Rice")
    print("Orders found:", len(search_result))

    if len(search_result) == 1:
        print("TEST PASSED!")
    else:
        print("TEST FAILED!")


def test_search_second_order():

    print("\n--- TEST 4: SEARCH SECOND ORDER ---")

    orders = load_orders()

    # Search for Nasi Lemak
    search = "Nasi Lemak".lower()
    search_result = []

    for order in orders:
        for item in order["items"]:
            if search in item["name"].lower():
                search_result.append(order)
                break

    print("Searching for: Nasi Lemak")
    print("Orders found:", len(search_result))

    if len(search_result) == 1:
        print("TEST PASSED!")
    else:
        print("TEST FAILED!")


def test_search_item_in_multiple_item_order():

    print("\n--- TEST 5: SEARCH ITEM IN MULTIPLE-ITEM ORDER ---")

    orders = load_orders()

    # Search for Iced Milo
    search = "Iced Milo".lower()
    search_result = []

    for order in orders:
        for item in order["items"]:
            if search in item["name"].lower():
                search_result.append(order)
                break

    print("Searching for: Iced Milo")
    print("Orders found:", len(search_result))

    if len(search_result) == 1:
        print("TEST PASSED!")
    else:
        print("TEST FAILED!")


def test_search_no_result():

    print("\n--- TEST 6: SEARCH WITH NO RESULT ---")

    orders = load_orders()

    # Search for an item that does not exist
    search = "Burger".lower()
    search_result = []

    for order in orders:
        for item in order["items"]:
            if search in item["name"].lower():
                search_result.append(order)
                break

    print("Searching for: Burger")
    print("Orders found:", len(search_result))

    if len(search_result) == 0:
        print("TEST PASSED!")
    else:
        print("TEST FAILED!")


def test_empty_storage():

    print("\n--- TEST 7: LOAD ORDER HISTORY ---")

    orders = load_orders()

    if isinstance(orders, list):
        print("Order history loaded successfully.")
        print("Number of orders:", len(orders))
        print("TEST PASSED!")
    else:
        print("TEST FAILED!")


if __name__ == "__main__":

    print("\n================================")
    print("       MEMBER 3 TESTING")
    print("================================")

    test_order_total()
    test_order_storage()
    test_search_order()
    test_search_second_order()
    test_search_item_in_multiple_item_order()
    test_search_no_result()
    test_empty_storage()

    print("\n================================")
    print("       TESTING COMPLETED")
    print("================================")