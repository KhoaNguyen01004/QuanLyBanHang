class Item:
    """
        Represents a single item with properties like name, ID, price, and category.

        This class provides a structured way to handle item-related data,
        including getters and setters for each of its attributes to ensure
        controlled access and modification.

        Attributes:
            __item_name (str): The name of the item.
            __item_id (str): A unique identifier for the item.
            __price (float): The price of the item.
        """

    def __init__(self, name: str, item_id: str, price: float):
        """
                Initializes a new Item instance.

                :param name: The name of the item.
                :param item_id: The unique ID of the item.
                :param price: The price of the item.
                """
        self.__item_name = name
        self.__item_id = item_id
        self.__price = price