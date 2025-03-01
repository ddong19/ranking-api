from ranking_api.models import Item
from typing import List

class ItemRepository:

    @staticmethod
    def get_item(self, item_id) -> Item:
        return Item.objects.get(id=item_id)

    @staticmethod
    def get_items(self, ranking_id: int) -> List[Item]:
        return list(Item.objects.filter(ranking_id = ranking_id).order_by('rank'))