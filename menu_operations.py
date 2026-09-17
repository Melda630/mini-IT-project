# Helper functions and Data Management for Menu Operations

menu_database = [
    {
        "id": 1, 
        "name": "Chicken Rice", 
        "category": "Main Meal", 
        "price": 6.50,
        "image": "chicken_rice.jpg"
    },
    {
        "id": 2, 
        "name": "Nasi Lemak Special", 
        "category": "Main Meal", 
        "price": 5.00,
        "image": "nasi_lemak.jpg"
    },
    {
        "id": 3, 
        "name": "Milo Ais", 
        "category": "Beverage", 
        "price": 2.50,
        "image": "milo_ais.jpg"
    },
    {
        "id": 4, 
        "name": "Teh Tarik", 
        "category": "Beverage", 
        "price": 2.00,
        "image": "teh_tarik.jpg"
    },
    {
        "id": 5, 
        "name": "Fried Mee Goreng", 
        "category": "Main Meal", 
        "price": 4.50,
        "image": "mee_goreng.jpg"
    }
]

next_item_id = 6


def get_all_items():
    """Returns the full list of menu items."""
    return menu_database


def filter_menu_items(category_filter="", search_query=""):
    """Filters menu items based on category and search text."""
    filtered = menu_database

    if category_filter:
        filtered = [
            item for item in filtered 
            if item["category"].lower() == category_filter.lower()
        ]

    if search_query:
        filtered = [
            item for item in filtered 
            if search_query.lower() in item["name"].lower()
        ]

    return filtered


def add_menu_item(name, category, price_str):
    """Adds a new menu item after validating inputs."""
    global next_item_id

    name = name.strip()
    category = category.strip()

    try:
        price = float(price_str)
    except (ValueError, TypeError):
        return False, "Invalid price format."

    if not name or not category or price <= 0:
        return False, "All fields are required and price must be greater than 0."

    new_item = {
        "id": next_item_id,
        "name": name,
        "category": category,
        "price": price,
        "image": ""  # Default empty image for newly added items
    }
    
    menu_database.append(new_item)
    next_item_id += 1
    return True, f"Successfully added '{name}' to the menu!"


def delete_menu_item_by_id(item_id):
    """Deletes an item from the menu by ID."""
    global menu_database
    item_to_delete = next((item for item in menu_database if item["id"] == item_id), None)

    if item_to_delete:
        menu_database = [item for item in menu_database if item["id"] != item_id]
        return True, f"Menu item '{item_to_delete['name']}' was deleted."
    
    return False, "Item not found."