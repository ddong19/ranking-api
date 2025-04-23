import pytest
from unittest.mock import Mock
from ranking_api.models.item import Item, RankingList
from ranking_api.repositories.item_repository import ItemRepository
from ranking_api.services.item_service import ItemService


class BaseTestItemService:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_item_repository = Mock(spec=ItemRepository)
        self.item_service = ItemService(item_repository=self.mock_item_repository)

class TestGetItem(BaseTestItemService):
    def test_get_item_success(self, fake_item):
        self.mock_item_repository.get_item.return_value = fake_item

        retrieved_item = self.item_service.get_item(fake_item.id)

        assert retrieved_item is not None
        assert retrieved_item.name == fake_item.name
        assert retrieved_item.notes == fake_item.notes
        assert retrieved_item.rank == fake_item.rank
        assert retrieved_item.ranking.title == fake_item.ranking.title
        self.mock_item_repository.get_item.assert_called_once_with(fake_item.id)


    def test_item_not_found(self, fake_item):
        self.mock_item_repository.get_item.return_value = None
        non_existent_ranking_id = 999
        retrieved_item = self.item_service.get_item(fake_item.id)

        assert retrieved_item is None
        self.mock_item_repository.get_item.assert_called_once_with(fake_item.id)

class TestGetAllItems(BaseTestItemService):
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

class TestCreateItem(BaseTestItemService):
    def test_create_item_with_name_success(self, fake_ranking):
        fake_item_name_only = Item(name="test", ranking_id=fake_ranking.id, rank=1)
        self.mock_item_repository.create_item.return_value = fake_item_name_only

        created_item = self.item_service.create_item(fake_item_name_only.name, fake_ranking.id)
        assert created_item.name == fake_item_name_only.name
        assert created_item.notes == fake_item_name_only.notes
        self.mock_item_repository.create_item.assert_called_once_with(fake_item_name_only.name, fake_ranking.id, fake_item_name_only.notes)

    def test_create_item_with_notes_success(self, fake_ranking, fake_item):
        self.mock_item_repository.create_item.return_value = fake_item

        created_item = self.item_service.create_item(fake_item.name, fake_ranking.id, fake_item.notes)
        assert created_item.name == fake_item.name
        assert created_item.notes == fake_item.notes
        self.mock_item_repository.create_item.assert_called_once_with(fake_item.name, fake_ranking.id, fake_item.notes)

class TestDeleteItem(BaseTestItemService):
    def test_delete_item_success(self):
        item_id = 1

        self.item_service.delete_item(item_id)

        self.mock_item_repository.delete_item.assert_called_once_with(item_id)

    def test_delete_item_not_found(self):
        item_id = 999
        self.mock_item_repository.delete_item.return_value = False
        exception_string = "Item with id " + str(item_id) + " does not exist."

        with pytest.raises(Exception, match=exception_string):
            self.item_service.delete_item(item_id)

        self.mock_item_repository.delete_item.assert_called_once_with(item_id)

class TestPatchItem(BaseTestItemService):
    def test_patch_item_success_with_name_and_notes(self, fake_item):
        updated_name = "Updated Name"
        updated_notes = "Updated Notes"
        self.mock_item_repository.patch_item.return_value = fake_item

        patched_item = self.item_service.patch_item(fake_item.id, name=updated_name, notes=updated_notes)

        assert patched_item is not None
        self.mock_item_repository.patch_item.assert_called_once_with(
            fake_item.id, name=updated_name, notes=updated_notes
        )

    def test_patch_item_success_with_name_only(self, fake_item):
        updated_name = "Name Only"
        self.mock_item_repository.patch_item.return_value = fake_item

        patched_item = self.item_service.patch_item(fake_item.id, name=updated_name)

        assert patched_item is not None
        self.mock_item_repository.patch_item.assert_called_once_with(
            fake_item.id, name=updated_name, notes=None
        )

    def test_patch_item_success_with_notes_only(self, fake_item):
        updated_notes = "Notes Only"
        self.mock_item_repository.patch_item.return_value = fake_item

        patched_item = self.item_service.patch_item(fake_item.id, notes=updated_notes)

        assert patched_item is not None
        self.mock_item_repository.patch_item.assert_called_once_with(
            fake_item.id, name=None, notes=updated_notes
        )

    def test_patch_item_not_found(self, fake_item):
        self.mock_item_repository.patch_item.return_value = None

        with pytest.raises(Item.DoesNotExist) as exc_info:
            self.item_service.patch_item(fake_item.id, name="Doesn't", notes="Matter")

        assert str(exc_info.value) == f"Item with id {fake_item.id} does not exist."
        self.mock_item_repository.patch_item.assert_called_once_with(
            fake_item.id, name="Doesn't", notes="Matter"
        )

class TestUpdateItemRanks(BaseTestItemService):
    def test_update_item_ranks_success(self):
        ranking_id = 1
        item_ids = [1, 2, 3]
        mock_items = [
            Item(id=1, ranking_id=1, rank=3),
            Item(id=2, ranking_id=1, rank=1),
            Item(id=3, ranking_id=1, rank=2),
        ]

        self.mock_item_repository.get_all_items.return_value = mock_items

        self.item_service.update_item_ranks(ranking_id, item_ids)

        self.mock_item_repository.get_all_items.assert_called_once_with(ranking_id)
        self.mock_item_repository.update_item_ranks.assert_called_once_with(item_ids)

    def test_update_item_ranks_fails_if_item_count_mismatch(self):
        ranking_id = 1
        item_ids = [1, 2, 3]
        # Only 2 items returned
        mock_items = [
            Item(id=1, ranking_id=1),
            Item(id=2, ranking_id=1),
        ]

        self.mock_item_repository.get_all_items.return_value = mock_items

        with pytest.raises(ValueError, match="Number of IDs given does not match number of items."):
            self.item_service.update_item_ranks(ranking_id, item_ids)

    def test_update_item_ranks_fails_if_wrong_ranking_id(self):
        ranking_id = 1
        item_ids = [1, 2, 3]
        mock_items = [
            Item(id=1, ranking_id=1),
            Item(id=2, ranking_id=2),
            Item(id=3, ranking_id=1),
        ]

        self.mock_item_repository.get_all_items.return_value = mock_items

        with pytest.raises(ValueError, match="All items must belong to the given ranking."):
            self.item_service.update_item_ranks(ranking_id, item_ids)

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



