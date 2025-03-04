import pytest
from unittest.mock import Mock
from ranking_api.models.item import Item, RankingList
from ranking_api.repositories.item_repository import ItemRepository
from ranking_api.services.item_service import ItemService


class TestItemService:
    def test_get_item_success(self, item_service, fake_item, mock_item_repository):
        mock_item_repository.get_item.return_value = fake_item

        retrieved_item = item_service.get_item(fake_item.ranking.id, fake_item.id)

        assert retrieved_item is not None
        assert retrieved_item.name == fake_item.name
        assert retrieved_item.notes == fake_item.notes
        assert retrieved_item.rank == fake_item.rank
        assert retrieved_item.ranking.title == fake_item.ranking.title
        mock_item_repository.get_item.assert_called_once_with(fake_item.ranking.id, fake_item.id)


    def test_item_not_found(self, item_service, fake_item, mock_item_repository):
        mock_item_repository.get_item.return_value = None
        non_existent_ranking_id = 999
        retrieved_item = item_service.get_item(non_existent_ranking_id, fake_item.id)

        assert retrieved_item is None
        mock_item_repository.get_item.assert_called_once_with(non_existent_ranking_id, fake_item.id)

    def test_get_items_success(self, item_service, fake_items_list, mock_item_repository):
        mock_item_repository.get_items.return_value = fake_items_list

        retrieved_items = item_service.get_items(fake_items_list[0].ranking.id)

        assert len(retrieved_items) == 2
        assert retrieved_items[0].name == fake_items_list[0].name
        assert retrieved_items[1].name == fake_items_list[1].name
        mock_item_repository.get_items.assert_called_once_with(fake_items_list[0].ranking.id)

    def test_get_items_wrong_ranking(self, item_service, mock_item_repository):
        mock_item_repository.get_items.return_value = None
        non_existent_ranking_id = 999
        retrieved_items = item_service.get_items(non_existent_ranking_id)

        assert retrieved_items is None
        mock_item_repository.get_items.assert_called_once_with(non_existent_ranking_id)


@pytest.fixture
def mock_item_repository():
    return Mock(spec=ItemRepository)

@pytest.fixture
def item_service(mock_item_repository):
    return ItemService(item_repository = mock_item_repository)

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



