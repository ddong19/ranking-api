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

    def create_item(self, name: str, ranking_id: int, notes: Optional[str] = None) -> Item:
        num_items = self.model.objects.filter(ranking_id=ranking_id).count()
        return self.model.objects.create(
            name = name,
            notes = notes if notes is not None else '',
            rank = num_items + 1,
            ranking_id = ranking_id,
        )
