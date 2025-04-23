import pytest
from ranking_api.models import Item, RankingList
from ranking_api.repositories.item_repository import ItemRepository

@pytest.mark.django_db
class TestItemRepository:
    class TestGetItem:
        def test_get_chicago_from_cities_ranking(self, repository, cities_ranking, cities_item):
            retrieved_item = repository.get_item(cities_item.id)

            assert retrieved_item is not None
            assert retrieved_item.name == "Chicago"
            assert retrieved_item.ranking.title == "Cities"

        def test_get_non_existent_item(self, repository, travel_ranking):
            retrieved_item = repository.get_item(999)

            assert retrieved_item is None

    class TestGetAllItems:
        def test_get_items_from_travel_ranking(self, repository, travel_ranking, travel_items):
            retrieved_items = repository.get_all_items(travel_ranking.id)

            assert len(retrieved_items) == 4

        def test_get_items_in_rank_order(self, repository, travel_ranking, travel_items):
            retrieved_items = repository.get_all_items(travel_ranking.id)

            assert retrieved_items[0].name == "London"
            assert retrieved_items[1].name == "Paris"
            assert retrieved_items[2].name == "Rome"
            assert retrieved_items[3].name == "Berlin"

    class TestCreateItem:
        def test_create_item_success(self, repository, cities_ranking, cities_item):
            item_name = "Ann Arbor"
            item_notes = "best school in the world"
            created_item = repository.create_item(item_name, 1, item_notes)

            assert created_item.name == item_name
            assert created_item.notes == item_notes
            assert created_item.rank == 2
            assert created_item.ranking_id == 1
            assert created_item.ranking.title == cities_ranking.title

        def test_create_item_with_no_notes(self, repository, cities_ranking, cities_item):
            item_name = "Ann Arbor"
            item_notes = None
            created_item = repository.create_item(item_name, 1, item_notes)

            assert created_item.name == item_name
            assert created_item.notes == ""
            assert created_item.rank == 2
            assert created_item.ranking_id == 1

        def test_create_multiple_items_with_correct_rank(self, repository, cities_ranking, cities_item):
            item1_name = "Ann Arbor"
            item1_notes = "best school in the world"

            item2_name = "Chicago"

            created_item1 = repository.create_item(item1_name, 1, item1_notes)
            created_item2 = repository.create_item(item2_name, 1)

            assert created_item1.name == item1_name
            assert created_item1.rank == 2
            assert created_item2.name == item2_name
            assert created_item2.rank == 3

    class TestDeleteItem:
        def test_delete_item_success(self, repository, cities_ranking, cities_item):
            response = repository.delete_item(cities_item.id)

            assert response is True
            assert Item.objects.filter(id=cities_item.id).exists() is False

        def test_delete_non_existent_item(self, repository):
            non_existent_id = 999

            response = repository.delete_item(non_existent_id)

            assert response is False

    class TestPatchItem:
        def test_patch_name_only(self, repository, cities_item):
            updated_item = repository.patch_item(item_id=cities_item.id, name="New York")

            assert updated_item is not None
            assert updated_item.name == "New York"
            assert updated_item.notes == cities_item.notes

        def test_patch_notes_only(self, repository, cities_item):
            new_notes = "Updated travel notes"
            updated_item = repository.patch_item(item_id=cities_item.id, notes=new_notes)

            assert updated_item is not None
            assert updated_item.notes == new_notes
            assert updated_item.name == cities_item.name

        def test_patch_both_fields(self, repository, cities_item):
            updated_item = repository.patch_item(
                item_id=cities_item.id,
                name="San Francisco",
                notes="Chilly in summer"
            )

            assert updated_item is not None
            assert updated_item.name == "San Francisco"
            assert updated_item.notes == "Chilly in summer"

        def test_patch_nonexistent_item(self, repository):
            updated_item = repository.patch_item(item_id=999, name="Ghost City")

            assert updated_item is None

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
        id = 1,
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
