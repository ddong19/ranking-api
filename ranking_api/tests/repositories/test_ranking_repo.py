import pytest

from ranking_api.models import RankingList
from ranking_api.repositories.ranking_repository import RankingRepository

@pytest.mark.django_db
class TestRankingRepository:

    def test_get_ranking(self, repository, ranking):
        retrieved_ranking = repository.get_ranking(ranking.id)

        assert retrieved_ranking is not None
        assert retrieved_ranking.title == ranking.title
        assert retrieved_ranking.description == ranking.description

    def test_get_non_existent_ranking(self, repository, ranking):
        retrieved_ranking = repository.get_ranking(999)

        assert retrieved_ranking is None

    def test_get_all_rankings(self, repository, ranking_list):
        retrieved_rankings = repository.get_all_rankings()

        assert len(retrieved_rankings) == 3
        assert retrieved_rankings[0].title == ranking_list[0].title
        assert retrieved_rankings[1].title == ranking_list[1].title
        assert retrieved_rankings[2].title == ranking_list[2].title

    def test_get_all_rankings_empty(self, repository):
        retrieved_rankings = repository.get_all_rankings()

        assert len(retrieved_rankings) == 0


@pytest.fixture
def ranking():
    return RankingList.objects.create(
        title="Travel Locations",
        description="The best places to visit",
    )

@pytest.fixture
def ranking_list():
    return [
        RankingList.objects.create(
            title="Travel Locations",
            description="The best places to visit",
        ),
        RankingList.objects.create(
            title="Cities",
            description="The best cities to visit",
        ),
        RankingList.objects.create(
            title="Restaurants",
            description="The best restaurants to visit",
        )
    ]

@pytest.fixture
def repository():
    return RankingRepository()