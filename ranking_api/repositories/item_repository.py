from ranking_api.models import Item
from typing import List, Optional

class ItemRepository:

    @staticmethod
    def get_item(ranking_id, item_id) -> Optional[Item]:
        try:
            return Item.objects.filter(ranking_id = ranking_id).get(id=item_id)
        except Item.DoesNotExist:
            return None

    @staticmethod
    def get_items(ranking_id) -> List[Item]:
        return list(Item.objects.filter(ranking_id = ranking_id).order_by('rank'))