class Hang:
    __item_name = ""
    __item_id = ""
    __price = 0
    __category = None

    def __init__(self, name: str, id: str, price: float, phan_loai: str):
        self.__item_name = name
        self.__item_id = id
        self.__price = price
        self.__category = phan_loai

    def get_item_name(self):
        return self.__item_name
    def set_item_name(self, name: str):
        self.__item_name = name

    def get_item_id(self):
        return self.__item_id
    def set_item_id(self, id: str):
        self.__item_id = id

    def get_price(self):
        return self.__price
    def set_price(self, price: float):
        self.__price = float

    def get_category(self):
        return self.__category
    def set_category(self, category: str|None):
        self.__category = category