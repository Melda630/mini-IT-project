from ordering import *

print("\n--- TEST 1: ADD ITEMS ---")

add_to_cart("Chicken Rice", 6.00, 2)
add_to_cart("Iced Milo", 2.50, 1)

view_cart()


print("\n--- TEST 2: MODIFY QUANTITY ---")


modify_quantity(1, 3)

view_cart()


print("\n--- TEST 3: INVALID QUANTITY ---")

modify_quantity(1, 0)


print("\n--- TEST 4: INVALID ITEM NUMBER ---")

remove_item(10)


print("\n--- TEST 5: REMOVE ITEM ---")

remove_item(2)

view_cart()


print("\n--- TEST 6: ADD SAME ITEM AGAIN ---")

add_to_cart("Chicken Rice", 6.00, 2)

view_cart()


print("\n--- TEST 7: CHECKOUT ---")

checkout()


print("\n--- TEST 8: ORDER HISTORY ---")

view_order_history()
