from django.db.models import F

from ranking_api.models import Item
from typing import List, Optional

class ItemRepository:
    def __init__(self):
        self.model = Item

    def get_item(self, item_id) -> Optional[Item]:
        try:
            return self.model.objects.get(
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

    def create_item(self, name: str, ranking_id: int, notes: Optional[str] = None, rank: Optional[int] = None) -> Item:
        return self.model.objects.create(
            name = name,
            notes = notes if notes is not None else '',
            rank = rank,
            ranking_id = ranking_id,
        )

    def count_items_in_ranking(self, ranking_id: int) -> int:
        return self.model.objects.filter(ranking_id=ranking_id).count()

    def shift_ranks_for_insert(self, ranking_id: int, insert_rank: int):
        self.model.objects.filter(
            ranking_id=ranking_id,
            rank__gte=insert_rank
        ).update(rank=F('rank') + 1)

    def shift_ranks_down(self, ranking_id: int, start: int, end: int):
        self.model.objects.filter(
            ranking_id=ranking_id,
            rank__gte=start,
            rank__lte=end
        ).update(rank=F('rank') + 1)

    def shift_ranks_up(self, ranking_id: int, start: int, end: Optional[int] = None):
        queryset = self.model.objects.filter(
            ranking_id=ranking_id,
            rank__gte=start
        )
        if end is not None:
            queryset = queryset.filter(rank__lte=end)

        queryset.update(rank=F('rank') - 1)

    def delete_item(self, item_id: int) -> bool:
        try:
            item = self.model.objects.get(id=item_id)
            item.delete()
            return True
        except self.model.DoesNotExist:
            return False

    def patch_item(self, item_id: int, name: str = None, notes: str = None):
        try:
            item = self.model.objects.get(id=item_id)
            if name is not None:
                item.name = name
            if notes is not None:
                item.notes = notes
            item.save()
            return item
        except self.model.DoesNotExist:
            return None