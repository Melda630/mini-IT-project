import unittest
from menu_operations import (
    menu_database,
    filter_menu_items,
    add_menu_item,
    delete_menu_item_by_id
)


class TestMenuOperations(unittest.TestCase):

    def test_filter_by_category(self):
        """Test filtering items by category."""
        results = filter_menu_items(category_filter="Beverage")
        for item in results:
            self.assertEqual(item["category"], "Beverage")

    def test_filter_by_search(self):
        """Test searching items by name keyword."""
        results = filter_menu_items(search_query="Rice")
        self.assertTrue(any("Rice" in item["name"] for item in results))

    def test_add_menu_item_success(self):
        """Test successfully adding a new menu item."""
        success, message = add_menu_item("Laksa", "Main Meal", "7.00")
        self.assertTrue(success)
        self.assertIn("Laksa", message)

    def test_add_menu_item_invalid_price(self):
        """Test adding item with invalid price."""
        success, message = add_menu_item("Roti Canai", "Main Meal", "invalid_price")
        self.assertFalse(success)

    def test_delete_menu_item(self):
        """Test deleting an existing menu item."""
        success, message = delete_menu_item_by_id(1)
        self.assertTrue(success)


if __name__ == "__main__":
    unittest.main()