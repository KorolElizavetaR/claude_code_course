from dto.ItemDto import ItemDto
from model.Item import Item


class ItemMapper:
    @staticmethod
    def dto_to_entity(dto: ItemDto):
        return Item(dto.name, dto.description)