from ranking_api.models import Item
from typing import List, Optional

class ItemRepository:
    def __init__(self):
        self.model = Item

    def get_item(self, ranking_id, item_id) -> Optional[Item]:
        try:
            return self.model.objects.get(
                ranking = ranking_id,
                id = item_id
            )
        except self.model.DoesNotExist:
            return None

    def get_all_items(self, ranking_id: int) -> List[Item]:
        return list(
            self.model.objects
            .filter(ranking=ranking_id)
            .order_by('rank')
        )
