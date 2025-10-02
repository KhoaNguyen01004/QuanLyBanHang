from __future__ import annotations
from item import Item


class Inventory:
    """
    Manages a collection of items with a dynamic size.

    This class provides core functionalities for managing an inventory,
    including adding, removing, and checking for the presence of items.
    It can be initialized with an optional list of existing items. The inventory
    has no size limit.

    Attributes:
        __list_of_items (list[Item]): A private list storing all the items in the inventory.
    """

    def __init__(self, list_of_items: list[Item] | None = None):
        """
        Initialize the inventory with an optional list of items.
        If no list is provided, the inventory starts empty.

        :param list_of_items: Optional list of Item objects.
        """
        if list_of_items is None:
            self.__list_of_items = []
        else:
            self.__list_of_items = list_of_items

    def add(self, item: Item):
        """
        Add an Item to the inventory.

        TODO:
            - Ensure each item has a unique ID.
            - Do not add the item if an item with the same ID already exists.
        """
        pass

    def remove(self, item: Item):
        """
        Remove an Item from the inventory if it exists.

        TODO:
            - Remove the given Item from __list_of_items.
            - If the Item does not exist, return None.
        """
        pass

    def remove_by_item_id(self, item_id: str):
        """
        Remove an Item from the inventory by its ID.

        TODO:
            - Find the Item with the given ID and remove it.
            - If the ID does not exist, return None.
        """
        pass

    def is_empty(self) -> bool:
        """
        Check if the inventory is empty.

        TODO:
            - Return True if the inventory has no items.
            - Return False otherwise.
        """
        pass

    def get_size(self) -> int:
        """
        Get the number of items in the inventory.

        TODO:
            - Return the size of __list_of_items.
        """
        pass

    def get_item_by_id(self, item_id: str) -> Item | None:
        """
        Retrieve an Item from the inventory by its ID.

        TODO:
            - Search for the Item with the given ID.
            - Return the Item if found, otherwise return None.
        """
        pass

    def __len__(self) -> int:
        """
        Return the number of items in the inventory.

        TODO:
            - Implement using the length of __list_of_items.
        """
        pass

    def __str__(self) -> str:
        """
        Return a string representation of the inventory.

        TODO:
            - Return a formatted string listing all items.
        """
        pass
