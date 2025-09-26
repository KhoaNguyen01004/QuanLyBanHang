import unittest
from Inventory import Inventory
from Item import Item


class InventoryTest(unittest.TestCase):

    def setUp(self):
        self.item1 = Item("Cá", "c1", 100.0)
        self.item2 = Item("Trứng", "tr1", 80.0)
        self.item3 = Item("Tôm", "t1", 200.0)

    def test_init_with_items(self):
        inventory = Inventory([self.item1, self.item2, self.item3])
        self.assertEqual(3, inventory.get_size())

    def test_init_with_size(self):
        inventory = Inventory(size=10)
        self.assertFalse(inventory.is_empty(), "Inventory chưa bỏ item nào hết nên phải trống")
        self.assertEqual(10, inventory.get_size())

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

if __name__ == '__main__':
    unittest.main()
