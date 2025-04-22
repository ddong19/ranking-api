from django.http import JsonResponse

from ranking_api.models import Item
from ranking_api.repositories.item_repository import ItemRepository
from typing import Optional


class ItemService:
    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository

    def get_item(self, item_id: int) -> Optional[Item]:
        return self.item_repository.get_item(item_id)

    def get_all_items(self, ranking_id: int) -> list[Item]:
        return self.item_repository.get_all_items(ranking_id)

    def create_item(self, name: str, ranking_id: int, notes: str = None):
        return self.item_repository.create_item(name, ranking_id, notes)

    def delete_item(self, item_id: int):
        deleted = self.item_repository.delete_item(item_id)
        if not deleted:
            raise Item.DoesNotExist(f"Item with id {item_id} does not exist.")