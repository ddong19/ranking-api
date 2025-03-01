import pytest
from ...models import Item, RankingList
from ...repositories.item_repository import ItemRepository
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'ranking_api.settings'



@pytest.mark.django_db
def test_get_item():
    ranking = RankingList.objects.create(
        title="Travel Locations",
        description="The best places to visit",
    )
    item1 = Item.objects.create(
        ranking=ranking,
        name="London",
        description="The capital of England",
    )
    item2 = Item.objects.create(
        ranking=ranking,
        name="Paris",
        description="The capital of France",
    )

    repo = ItemRepository()
    items = repo.get_items(ranking.id)

    assert len(items) == 2
    assert items[0].name == item1.name
    assert items[1].name == item2.name

