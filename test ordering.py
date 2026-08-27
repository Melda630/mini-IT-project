from ordering import *

# Test adding items
add_to_cart("Chicken Rice", 6.00, 2)
add_to_cart("Iced Milo", 2.50, 1)

# Display cart
view_cart()

# Test modifying quantity
print("\n--- Modifying Chicken Rice quantity ---")
modify_quantity(1, 3)
view_cart()

# Test removing item
print("\n--- Removing Iced Milo ---")
remove_item(2)
view_cart()

# Test checkout
checkout()