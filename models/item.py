from typing import Any

class Item:
    """
    Represents a single item with properties like name, ID, and price.

    This class provides a structured way to handle item-related data and
    includes a robust comparison method for object equality.

    Attributes:
        _name (str): The name of the item.
        _item_id (str): A unique identifier for the item.
        _price (float): The price of the item.
    """

    def __init__(self, name: str, item_id: str, price: float):
        """
        Initializes a new Item instance.

        :param name: The name of the item.
        :param item_id: The unique ID of the item.
        :param price: The price of the item.
        """
        self._name = name
        self._item_id = item_id
        self._price = price

    def __eq__(self, other: Any) -> bool:
        """
        Compares two Item objects for equality based on their item_id.

        This method follows the Pythonic convention of returning
        NotImplemented for mismatched types.

        :param other: The object to compare with.
        :return: True if the objects are equal by ID, False otherwise.
        """
        if not isinstance(other, Item):
            return NotImplemented
        return self._item_id == other._item_id

    def __hash__(self) -> int:
        """
        Makes Item objects hashable based on their item_id.

        This allows items to be used in sets or as dictionary keys.
        """
        return hash(self._item_id)

    def get_id(self):
        """
        Get the id of an item

        :return: id of an item

        """
        return self._item_id

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the Item.

        :return: A string showing the name, ID, and price.
                 Example: "Item(name='Cá', id='c1', price=100.0)"
        """
        return f"Item(name='{self._name}', id='{self._item_id}', price={self._price})"

    def __repr__(self) -> str:
        """
        Return the official string representation of the Item.

        This is mainly for debugging and logging, and by default
        it mirrors the __str__ output.

        :return: A string representation of the item.
        """
        return self.__str__()

    def get_name(self) -> str:
        """
        Get the name of the item.

        :return: The item's name as a string.
        """
        return self._name

    def get_price(self) -> float:
        """
        Get the price of the item.

        :return: The item's price as a float.
        """
        return self._price
