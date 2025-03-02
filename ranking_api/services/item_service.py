from ranking_api.models import Item
from repositories.item_repository import ItemRepository


class ItemService:
    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository

    def get_item(self, ranking_id, item_id) -> Item:
        return self.item_repository.get_item(ranking_id, item_id)

    def get_items(self, ranking_id) -> list[Item]:
        return self.item_repository.get_items(ranking_id)