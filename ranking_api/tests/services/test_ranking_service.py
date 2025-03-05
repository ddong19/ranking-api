import pytest
from unittest.mock import Mock

from ranking_api.models import RankingList
from ranking_api.repositories.ranking_repository import RankingRepository
from ranking_api.services.ranking_service import RankingService


class TestRankingService:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_ranking_repository = Mock(spec=RankingRepository)
        self.ranking_service = RankingService(ranking_repository=self.mock_ranking_repository)


    def test_get_ranking_success(self, fake_ranking):
        self.mock_ranking_repository.get_ranking.return_value = fake_ranking

        retrieved_ranking = self.ranking_service.get_ranking(fake_ranking.id)

        assert retrieved_ranking is not None
        assert retrieved_ranking.title == fake_ranking.title
        assert retrieved_ranking.description == fake_ranking.description
        self.mock_ranking_repository.get_ranking.assert_called_once_with(fake_ranking.id)

    def test_get_ranking_not_found(self):
        self.mock_ranking_repository.get_ranking.return_value = None
        non_existent_ranking_id = 999

        retrieved_ranking = self.ranking_service.get_ranking(non_existent_ranking_id)

        assert retrieved_ranking is None
        self.mock_ranking_repository.get_ranking.assert_called_once_with(non_existent_ranking_id)

    def test_get_all_rankings(self, fake_ranking_list):
        self.mock_ranking_repository.get_all_rankings.return_value = fake_ranking_list

        retrieved_rankings = self.ranking_service.get_all_rankings()

        assert len(retrieved_rankings) == 3
        assert retrieved_rankings[0].title == fake_ranking_list[0].title
        assert retrieved_rankings[1].title == fake_ranking_list[1].title
        assert retrieved_rankings[2].title == fake_ranking_list[2].title
        self.mock_ranking_repository.get_all_rankings.assert_called_once()


@pytest.fixture
def fake_ranking():
    return RankingList(
        title = "test title",
        description = "test description",
    )

@pytest.fixture
def fake_ranking_list():
    return [
        RankingList(
            title = "test title 1",
            description = "test description 1",
        ),
        RankingList(
            title = "test title 2",
            description = "test description 2",
        ),
        RankingList(
            title = "test title 3",
            description = "test description 3",
        )
    ]
