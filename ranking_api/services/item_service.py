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

    def create_item(self, name: str, ranking_id: int, notes: str = None, rank: Optional[int] = None):
        if rank is None:
            rank = self.item_repository.count_items_in_ranking(ranking_id)
        else:
            self.item_repository.shift_ranks_for_insert(ranking_id, rank)

        return self.item_repository.create_item(name, ranking_id, notes, rank)

    def delete_item(self, item_id: int):
        deleted = self.item_repository.delete_item(item_id)
        if not deleted:
            raise Item.DoesNotExist(f"Item with id {item_id} does not exist.")

    def patch_item(self, item_id: int, name: str = None, notes: str = None):
        patched_item = self.item_repository.patch_item(item_id, name=name, notes=notes)
        if not patched_item:
            raise Item.DoesNotExist(f"Item with id {item_id} does not exist.")
        return patched_item

    def update_item_rank(self, item_id: int, new_rank: int) -> Item:
        item = self.item_repository.get_item(item_id)
        if item.rank == new_rank:
            return item  # No change

        if new_rank < item.rank:
            # Item is moving up
            self.item_repository.shift_ranks_down(
                ranking_id=item.ranking_id,
                start=new_rank,
                end=item.rank - 1
            )
        else:
            # Item is moving down
            self.item_repository.shift_ranks_up(
                ranking_id=item.ranking_id,
                start=item.rank + 1,
                end=new_rank
            )

        item.rank = new_rank
        item.save()
        return item