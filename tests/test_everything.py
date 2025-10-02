import unittest
from models.inventory import Inventory
from models.item import Item
from models.shopping_cart import Cart


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.item1 = Item("Cá", "c1", 100.0)
        self.item2 = Item("Trứng", "tr1", 80.0)
        self.item3 = Item("Tôm", "t1", 200.0)

    def test_init_with_items(self):
        inventory = Inventory([self.item1, self.item2, self.item3])
        self.assertEqual(3, inventory.get_size())

    def test_init_with_size(self):
        inventory = Inventory()
        self.assertTrue(inventory.is_empty(), "Inventory chưa bỏ item nào hết nên phải trống")
        self.assertEqual(0, inventory.get_size(), "Vì Inventory chưa có item nào được bỏ vô nên size phải bằng 0")

    def test_get_size(self):
        inventory1 = Inventory(list_of_items=[self.item1, self.item2, self.item3])
        self.assertEqual(3, inventory1.get_size())
        inventory2 = Inventory()
        self.assertEqual(0, inventory2.get_size())

    def test_add(self):
        inventory = Inventory()
        inventory.add(self.item1)
        self.assertEqual(1, inventory.get_size())
        inventory.add(self.item3)
        self.assertEqual(2, inventory.get_size())

    def test_remove(self):
        inventory = Inventory(list_of_items=[self.item1, self.item2, self.item3])
        inventory.remove(self.item1)
        self.assertEqual(2, inventory.get_size())
        inventory.remove(self.item3)
        self.assertEqual(1, inventory.get_size())
        self.assertIsNone(inventory.remove(Item("Banana", "b01", 100)))

    def test_remove_id(self):
        inventory = Inventory(list_of_items=[self.item1, self.item2, self.item3])
        inventory.remove_by_item_id("c1")
        self.assertEqual(2, inventory.get_size())
        self.assertIsNone(inventory.get_item_by_id("aaa"))

class TestCart(unittest.TestCase):

    def setUp(self):
        self.item1 = Item("Cá", "c1", 100.0)
        self.item2 = Item("Trứng", "tr1", 80.0)
        self.item3 = Item("Tôm", "t1", 200.0)

    def test_init_empty(self):
        cart = Cart()
        self.assertTrue(cart.is_empty(), "Cart should be empty on initialization")
        self.assertEqual(0, len(cart))

    def test_add_single_item(self):
        cart = Cart()
        cart.add(self.item1)
        self.assertFalse(cart.is_empty())
        self.assertEqual(1, len(cart))
        self.assertEqual(self.item1, cart.get_item("c1"))

    def test_add_multiple_items(self):
        cart = Cart()
        cart.add_list_items([self.item1, self.item2])
        self.assertEqual(2, len(cart))
        self.assertEqual(self.item2, cart.get_item("tr1"))

    def test_remove_item(self):
        cart = Cart()
        cart.add_list_items([self.item1, self.item2, self.item3])
        removed = cart.remove(self.item1)
        self.assertTrue(removed, "Item should be removed successfully")
        self.assertEqual(2, len(cart))
        self.assertIsNone(cart.get_item("c1"))

        removed_nonexistent = cart.remove(Item("Banana", "b01", 50.0))
        self.assertFalse(removed_nonexistent, "Removing a non-existent item should return False")

    def test_remove_by_id(self):
        cart = Cart()
        cart.add_list_items([self.item1, self.item2])
        removed = cart.remove_by_id("tr1")
        self.assertTrue(removed, "Item should be removed by id successfully")
        self.assertEqual(1, len(cart))
        self.assertIsNone(cart.get_item("tr1"))

        removed_nonexistent = cart.remove_by_id("fake_id")
        self.assertFalse(removed_nonexistent, "Removing by non-existent id should return False")

    def test_get_item(self):
        cart = Cart()
        cart.add(self.item3)
        found_item = cart.get_item("t1")
        self.assertEqual(self.item3, found_item)
        not_found_item = cart.get_item("x1")
        self.assertIsNone(not_found_item)

    def test_str_representation(self):
        cart = Cart()
        cart.add_list_items([self.item1, self.item2])
        cart_str = str(cart)
        self.assertIn("Cá", cart_str)
        self.assertIn("Trứng", cart_str)


if __name__ == '__main__':
    unittest.main()
