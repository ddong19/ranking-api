import pytest
from ranking_api.models import Item, RankingList
from ranking_api.repositories.item_repository import ItemRepository

@pytest.mark.django_db
class TestItemRepository:

    def test_get_chicago_from_cities_ranking(self, repository, cities_ranking, cities_item):
        retrieved_item = repository.get_item(cities_ranking.id, cities_item.id)

        assert retrieved_item is not None
        assert retrieved_item.name == "Chicago"
        assert retrieved_item.ranking.title == "Cities"

    def test_get_chicago_from_wrong_ranking(self, repository, travel_ranking, cities_item):
        retrieved_item = repository.get_item(travel_ranking.id, cities_item.id)

        assert retrieved_item is None

    def test_get_items_from_travel_ranking(self, repository, travel_ranking, travel_items):
        retrieved_items = repository.get_all_items(travel_ranking.id)

        assert len(retrieved_items) == 4


    def test_get_items_in_rank_order(self, repository, travel_ranking, travel_items):
        retrieved_items = repository.get_all_items(travel_ranking.id)

        assert retrieved_items[0].name == "London"
        assert retrieved_items[1].name == "Paris"
        assert retrieved_items[2].name == "Rome"
        assert retrieved_items[3].name == "Berlin"

@pytest.fixture
def repository():
    return ItemRepository()

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
        ),
        Item.objects.create(
            ranking=travel_ranking,
            name="Berlin",
            notes="The capital of Germany",
            rank=4
        ),
        Item.objects.create(
            ranking=travel_ranking,
            name="Rome",
            notes="The capital of Italy",
            rank=3
        )
    ]

@pytest.fixture
def cities_item(cities_ranking):
    return Item.objects.create(
        ranking=cities_ranking,
        name="Chicago",
        rank=1
    )
