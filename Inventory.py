from Item import Item


#TODO Implement this class, remove "pass" when implement
class Inventory:
    """
    Manages a collection of items with a fixed or dynamic size.

    This class provides core functionalities for managing an inventory,
    including adding, removing, and checking for the presence of items.
    It can be initialized with an optional list of existing items and a
    specified size. If the size is 0, the inventory has unlimited capacity.

    Attributes:
        __list_of_items (list[Item]): A private list storing all the items in the inventory.
        __size (int): The maximum number of items the inventory can hold. A value of 0 indicates no size limit.
    """


    def __init__(self, list_of_items: list|None=None, size: int=0):
        """
        Initialized an empty list of item with default size of 0
        :param list_of_items: Items to be added, could be None
        :param size: Size of the list
        """
        self.__size = size
        self.__list_of_items = list_of_items

    def add(self, item: Item):
        #TODO thêm object Item vào lists_of_items
        pass

    def remove(self, item: Item):
        #TODO xóa object Item ra khỏi lists_of_items nếu Item đó có tồn tại trong __list_of_items.
        # Nếu item không tồn tại trong list, trả về None
        pass

    def remove_by_item_id(self, item_id: str):
        #TODO xóa object Item theo ID của item nếu id được tìm thấy trong __list_of_items.
        # Nếu item_id không tồn tại trong list, trả về None
        pass

    def is_empty(self) -> bool:
        #TODO trả về true nếu list rỗng, trả về false nếu list có ít nhất 1 item
        pass

    def get_size(self) -> int:
        #TODO trả về số lượng items trong __list_of_items
        pass

    def get_item_by_id(self, item_id: str) -> Item|None:
        #TODO tìm kiếm item theo id. Nếu item có trong __list_of_items return item đó, nếu không có return None
        pass