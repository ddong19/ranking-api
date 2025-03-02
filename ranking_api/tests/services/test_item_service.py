import pytest
from unittest.mock import Mock, patch
from typing import Optional

from ranking_api.models.item import Item, RankingList
from ranking_api.repositories.item_repository import ItemRepository
from ranking_api.services.item_service import ItemService


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

