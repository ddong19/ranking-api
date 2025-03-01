import pytest
from ranking_api.models import Item, RankingList
from ranking_api.repositories.item_repository import ItemRepository

@pytest.mark.django_db
def test_get_item():
    ranking = RankingList.objects.create(
        title="Travel Locations",
        description="The best places to visit",
    )
    item1 = Item.objects.create(
        ranking=ranking,
        name="London",
        notes="The capital of England",
        rank=1
    )
    item2 = Item.objects.create(
        ranking=ranking,
        name="Paris",
        notes="The capital of France",
        rank=2
    )

    repo = ItemRepository()
    items = repo.get_items(ranking.id)

    assert len(items) == 2
    assert items[0].name == item1.name
    assert items[1].name == item2.name

