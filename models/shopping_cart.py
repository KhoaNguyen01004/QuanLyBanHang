from models.item import Item

class Cart:
    """
    A shopping cart that holds a collection of Item objects.

    The Cart supports adding, removing, and retrieving items.
    It behaves like a dynamic container with no fixed size.
    """

    def __init__(self):
        """
        Initialize an empty cart.
        """
        self._cart = []

    def is_empty(self) -> bool:
        """
        Check if the cart is empty.

        :return: True if the cart has no items, False otherwise.
        """
        return len(self._cart) == 0

    def add(self, item: Item) -> None:
        """
        Add a single item to the cart.

        :param item: The Item object to be added.
        """
        self._cart.append(item)

    def add_list_items(self, list_of_items: list[Item]) -> None:
        """
        Add multiple items to the cart at once.

        :param list_of_items: A list of Item objects to be added.
        """
        self._cart.extend(list_of_items)

    def remove(self, item: Item) -> bool:
        """
        Remove an item from the cart if it exists.

        :param item: The Item object to remove.
        :return: True if the item was removed, False if not found.
        """
        if item in self._cart:
            self._cart.remove(item)
            return True
        return False

    def remove_by_id(self, item_id: str) -> bool:
        """
        Remove an item from the cart by its ID.

        :param item_id: The ID of the item to remove.
        :return: True if an item with the given ID was removed, False otherwise.
        """
        for item in self._cart:
            if item.get_id() == item_id:
                self._cart.remove(item)
                return True
        return False

    def get_item(self, item_id: str) -> Item|None:
        """
        Get the item in shopping cart by id if found

        :param item_id: the id string to be searched for
        :return: item if it's id is found, None otherwise
        """
        for item in self._cart:
            if item.get_id() == item_id:
                return item
        return None

    def __len__(self) -> int:
        """
        Get the number of items currently in the cart.

        :return: The number of items in the cart.
        """
        return len(self._cart)

    def __str__(self) -> str:
        """
        Get a string representation of the cart.

        :return: A string containing all items in the cart.
        """
        return f"Cart({[str(item) for item in self._cart]})"
