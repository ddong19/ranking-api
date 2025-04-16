import pytest
from unittest.mock import Mock
from ranking_api.models.item import Item, RankingList
from ranking_api.repositories.item_repository import ItemRepository
from ranking_api.services.item_service import ItemService


class TestItemService:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_item_repository = Mock(spec=ItemRepository)
        self.item_service = ItemService(item_repository=self.mock_item_repository)

    def test_get_item_success(self, fake_item):
        self.mock_item_repository.get_item.return_value = fake_item

        retrieved_item = self.item_service.get_item(fake_item.ranking.id, fake_item.id)

        assert retrieved_item is not None
        assert retrieved_item.name == fake_item.name
        assert retrieved_item.notes == fake_item.notes
        assert retrieved_item.rank == fake_item.rank
        assert retrieved_item.ranking.title == fake_item.ranking.title
        self.mock_item_repository.get_item.assert_called_once_with(fake_item.ranking.id, fake_item.id)


    def test_item_not_found(self, fake_item):
        self.mock_item_repository.get_item.return_value = None
        non_existent_ranking_id = 999
        retrieved_item = self.item_service.get_item(non_existent_ranking_id, fake_item.id)

        assert retrieved_item is None
        self.mock_item_repository.get_item.assert_called_once_with(non_existent_ranking_id, fake_item.id)


    def test_get_items_success(self, fake_items_list):
        self.mock_item_repository.get_all_items.return_value = fake_items_list

        retrieved_items = self.item_service.get_all_items(fake_items_list[0].ranking.id)

        assert len(retrieved_items) == 2
        assert retrieved_items[0].name == fake_items_list[0].name
        assert retrieved_items[1].name == fake_items_list[1].name
        self.mock_item_repository.get_all_items.assert_called_once_with(fake_items_list[0].ranking.id)


    def test_get_items_wrong_ranking(self):
        self.mock_item_repository.get_all_items.return_value = None
        non_existent_ranking_id = 999
        retrieved_items = self.item_service.get_all_items(non_existent_ranking_id)

        assert retrieved_items is None
        self.mock_item_repository.get_all_items.assert_called_once_with(non_existent_ranking_id)


@pytest.fixture
def fake_ranking():
    return RankingList(
        title = "test title",
        description = "test description",
    )

@pytest.fixture
def fake_item(fake_ranking):
    return Item(
        name = "test item",
        notes = "test notes",
        rank = 1,
        ranking = fake_ranking,
    )

@pytest.fixture
def fake_items_list(fake_ranking):
    return [
        Item(
            name = "test item 1",
            notes = "test notes 1",
            rank = 1,
            ranking = fake_ranking,
        ),
        Item(
            name = "test item 2",
            notes = "test notes 2",
            rank = 2,
            ranking = fake_ranking,
        )
    ]



