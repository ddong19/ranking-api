import pytest
from ranking_api.models import Item, RankingList
from ranking_api.repositories.item_repository import ItemRepository


@pytest.mark.django_db
def test_get_items_from_travel_ranking(travel_ranking, travel_items):
    repo = ItemRepository()
    retrieved_items = repo.get_items(travel_ranking.id)

    assert len(retrieved_items) == 2
    assert retrieved_items[0].name == "London"
    assert retrieved_items[1].name == "Paris"


@pytest.mark.django_db
def test_get_chicago_from_cities_ranking(cities_ranking, cities_item):
    repo = ItemRepository()
    retrieved_item = repo.get_item(cities_ranking.id, cities_item.id)

    assert retrieved_item is not None
    assert retrieved_item.name == "Chicago"
    assert retrieved_item.ranking.title == "Cities"


@pytest.mark.django_db
def test_get_chicago_from_wrong_ranking(travel_ranking, cities_item):
    repo = ItemRepository()
    retrieved_item = repo.get_item(travel_ranking.id, cities_item.id)

    assert retrieved_item is None


@pytest.fixture
def travel_ranking():
    return RankingList.objects.create(
        title="Travel Locations",
        description="The best places to visit",
    )

@pytest.fixture
def cities_ranking():
    return RankingList.objects.create(
        title="Cities",
        description="The best cities to visit",
    )

@pytest.fixture
def travel_items(travel_ranking):
    return [
        Item.objects.create(
            ranking=travel_ranking,
            name="London",
            notes="The capital of England",
            rank=1
        ),
        Item.objects.create(
            ranking=travel_ranking,
            name="Paris",
            notes="The capital of France",
            rank=2
        )
    ]

@pytest.fixture
def cities_item(cities_ranking):
    return Item.objects.create(
        ranking=cities_ranking,
        name="Chicago",
        rank=1
    )
