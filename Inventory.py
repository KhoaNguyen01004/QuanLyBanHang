from __future__ import annotations

from Item import Item


#TODO Implement this class, remove "pass" when implement, make sure to include docstrings
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


    def __init__(self, list_of_items: list|None=None):
        """
        Initialized an empty list of item with default size of 0
        :param list_of_items: Items to be added, could be None
        """
        if list_of_items is None:
            self.__list_of_items = []
            self._size = 0
        else:
            self.__list_of_items = list_of_items
            self._size = len(list_of_items)

    def add(self, item: Item):
        #TODO thêm object Item vào lists_of_items. Tất cả item chỉ được duy nhất 1 id và
        # không trùng với id của item khác
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
        pass

    def get_item_by_id(self, item_id: str) -> Item|None:
        #TODO tìm kiếm item theo id. Nếu item có trong __list_of_items return item đó, nếu không có return None
        pass