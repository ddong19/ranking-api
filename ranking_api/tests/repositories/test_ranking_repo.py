import pytest

from ranking_api.models import RankingList
from ranking_api.repositories.ranking_repository import RankingRepository

@pytest.mark.django_db
class TestRankingRepository:
    class TestGetRanking:
        def test_get_ranking_success(self, repository, ranking):
            retrieved_ranking = repository.get_ranking(ranking.id)

            assert retrieved_ranking is not None
            assert retrieved_ranking.title == ranking.title
            assert retrieved_ranking.description == ranking.description

        def test_get_non_existent_ranking(self, repository):
            retrieved_ranking = repository.get_ranking(999)

            assert retrieved_ranking is None

    class TestGetAllRankings:
        def test_get_all_rankings_success(self, repository, ranking_list):
            retrieved_rankings = repository.get_all_rankings()

            assert len(retrieved_rankings) == 3
            assert retrieved_rankings[0].title == ranking_list[0].title
            assert retrieved_rankings[1].title == ranking_list[1].title
            assert retrieved_rankings[2].title == ranking_list[2].title

        def test_get_all_rankings_empty(self, repository):
            retrieved_rankings = repository.get_all_rankings()

            assert len(retrieved_rankings) == 0

    class TestCreateRanking:
        def test_create_ranking(self, repository):
            ranking_title = "Travel Locations"
            ranking_description = "The best places to visit"

            retrieved_ranking = repository.create_ranking(ranking_title, ranking_description)

            assert retrieved_ranking.title == ranking_title
            assert retrieved_ranking.description == ranking_description

            db_ranking = RankingList.objects.get(id=retrieved_ranking.id)
            assert db_ranking.title == ranking_title
            assert db_ranking.description == ranking_description

        def test_create_ranking_with_title_only(self, repository):
            ranking = repository.create_ranking(title="Test Ranking")

            assert ranking.title == "Test Ranking"
            assert ranking.description == ""

            db_ranking = RankingList.objects.get(id=ranking.id)
            assert db_ranking.title == "Test Ranking"
            assert db_ranking.description == ""

        def test_create_ranking_with_none_description(self, repository):
            ranking = repository.create_ranking(
                title="Test Ranking",
                description=None
            )

            assert ranking.title == "Test Ranking"
            assert ranking.description == ""

            db_ranking = RankingList.objects.get(id=ranking.id)
            assert db_ranking.title == "Test Ranking"
            assert db_ranking.description == ""


@pytest.fixture
def repository():
    return RankingRepository()

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