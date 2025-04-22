import pytest
from unittest.mock import Mock

from ranking_api.models import RankingList
from ranking_api.repositories.ranking_repository import RankingRepository
from ranking_api.services.ranking_service import RankingService


class BaseTestRankingService:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_ranking_repository = Mock(spec=RankingRepository)
        self.ranking_service = RankingService(ranking_repository=self.mock_ranking_repository)


class TestGetRanking(BaseTestRankingService):
    def test_get_ranking_success(self, fake_ranking):
        self.mock_ranking_repository.get_ranking.return_value = fake_ranking

        retrieved_ranking = self.ranking_service.get_ranking(fake_ranking.id)

        assert retrieved_ranking is not None
        assert retrieved_ranking.id == fake_ranking.id
        assert retrieved_ranking.title == fake_ranking.title
        assert retrieved_ranking.description == fake_ranking.description
        self.mock_ranking_repository.get_ranking.assert_called_once_with(fake_ranking.id)

    def test_get_ranking_not_found(self):
        self.mock_ranking_repository.get_ranking.return_value = None
        non_existent_ranking_id = 999

        retrieved_ranking = self.ranking_service.get_ranking(non_existent_ranking_id)

        assert retrieved_ranking is None
        self.mock_ranking_repository.get_ranking.assert_called_once_with(non_existent_ranking_id)


class TestGetAllRankings(BaseTestRankingService):
    def test_get_all_rankings(self, fake_ranking_list):
        self.mock_ranking_repository.get_all_rankings.return_value = fake_ranking_list

        retrieved_rankings = self.ranking_service.get_all_rankings()

        assert len(retrieved_rankings) == 3
        assert retrieved_rankings[0].title == fake_ranking_list[0].title
        assert retrieved_rankings[1].title == fake_ranking_list[1].title
        assert retrieved_rankings[2].title == fake_ranking_list[2].title
        self.mock_ranking_repository.get_all_rankings.assert_called_once()


class TestCreateRanking(BaseTestRankingService):
    def test_create_ranking_with_title_only(self):
        expected_ranking = RankingList(title="Test Title")
        self.mock_ranking_repository.create_ranking.return_value = expected_ranking

        result = self.ranking_service.create_ranking(title="Test Title")

        self.mock_ranking_repository.create_ranking.assert_called_once_with("Test Title", None)
        assert result == expected_ranking

    def test_create_ranking_with_title_and_description(self):
        expected_ranking = RankingList(title="Test Title", description="Test Description")
        self.mock_ranking_repository.create_ranking.return_value = expected_ranking

        result = self.ranking_service.create_ranking(
            title="Test Title",
            description="Test Description"
        )

        self.mock_ranking_repository.create_ranking.assert_called_once_with(
            "Test Title",
            "Test Description"
        )
        assert result == expected_ranking

class TestDeleteRanking(BaseTestRankingService):
    def test_delete_ranking_success(self):
        ranking_id = 1

        self.ranking_service.delete_ranking(ranking_id)

        self.mock_ranking_repository.delete_ranking.assert_called_once_with(ranking_id)

    def test_delete_ranking_not_found(self):
        ranking_id = 999
        self.mock_ranking_repository.delete_ranking.return_value = False
        exception_string = "Ranking with id " + str(ranking_id) + " does not exist."

        with pytest.raises(Exception, match=exception_string):
            self.ranking_service.delete_ranking(ranking_id)

        self.mock_ranking_repository.delete_ranking.assert_called_once_with(ranking_id)

class TestUpdateRanking(BaseTestRankingService):
    def test_update_ranking_success(self):
        ranking_id = 1
        title = "Updated Title"
        description = "Updated Description"

        updated_ranking = RankingList(id=ranking_id, title=title, description=description)
        self.mock_ranking_repository.update_ranking.return_value = updated_ranking

        result = self.ranking_service.update_ranking(ranking_id, title, description)

        self.mock_ranking_repository.update_ranking.assert_called_once_with(ranking_id, title, description)
        assert result == updated_ranking

    def test_update_ranking_not_found_propagates_exception(self):
        ranking_id = 999
        title = "New Title"
        description = "New Description"
        self.mock_ranking_repository.update_ranking.return_value = None

        with pytest.raises(Exception, match="Failed to update ranking:"):
            self.ranking_service.update_ranking(ranking_id, title, description)

        self.mock_ranking_repository.update_ranking.assert_called_once_with(ranking_id, title, description)

    def test_update_ranking_with_title_only(self):
        ranking_id = 1
        title = "Updated Title"

        updated_ranking = RankingList(id=ranking_id, title=title, description="")
        self.mock_ranking_repository.update_ranking.return_value = updated_ranking

        result = self.ranking_service.update_ranking(ranking_id, title)

        self.mock_ranking_repository.update_ranking.assert_called_once_with(ranking_id, title, None)
        assert result == updated_ranking



@pytest.fixture
def fake_ranking():
    return RankingList(
        id = 1,
        title="test title",
        description="test description",
    )


@pytest.fixture
def fake_ranking_list():
    return [
        RankingList(
            title="test title 1",
            description="test description 1",
        ),
        RankingList(
            title="test title 2",
            description="test description 2",
        ),
        RankingList(
            title="test title 3",
            description="test description 3",
        )
    ]
