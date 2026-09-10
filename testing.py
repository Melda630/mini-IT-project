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
        }
    ]

    save_orders(test_orders)

    loaded_orders = load_orders()

    if loaded_orders == test_orders:
        print("TEST PASSED!")
    else:
        print("TEST FAILED!")


def test_empty_storage():

    print("\n--- TEST 3: LOAD ORDER HISTORY ---")

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
    test_empty_storage()

    print("\n================================")
    print("       TESTING COMPLETED")
    print("================================")