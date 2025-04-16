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

            ranking = repository.create_ranking(ranking_title, ranking_description)

            assert ranking.title == ranking_title
            assert ranking.description == ranking_description

            db_ranking = RankingList.objects.get(id=ranking.id)
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

    class TestDeleteRanking:
        def test_delete_ranking_success(self, repository, ranking):
            response = repository.delete_ranking(ranking.id)

            assert response is True
            assert RankingList.objects.filter(id=ranking.id).exists() is False

        def test_delete_non_existent_ranking(self, repository):
            non_existent_id = 999

            response = repository.delete_ranking(non_existent_id)

            assert response is False

    class TestUpdateRanking:
        def test_update_ranking_success(self, repository, ranking):
            new_title = "Updated Travel Locations"
            new_description = "The updated places to visit"

            updated_ranking = repository.update_ranking(
                ranking.id,
                new_title,
                new_description
            )

            assert updated_ranking is not None
            assert updated_ranking.title == new_title
            assert updated_ranking.description == new_description

            db_ranking = RankingList.objects.get(id=ranking.id)
            assert db_ranking.title == new_title
            assert db_ranking.description == new_description

        def test_update_ranking_with_title_only(self, repository, ranking):
            new_title = "Updated Travel Locations"

            updated_ranking = repository.update_ranking(
                ranking.id,
                title=new_title
            )

            assert updated_ranking is not None
            assert updated_ranking.title == new_title
            assert updated_ranking.description == ""

            db_ranking = RankingList.objects.get(id=ranking.id)
            assert db_ranking.title == new_title
            assert db_ranking.description == ""

        def test_update_ranking_with_none_description(self, repository, ranking):
            new_title = "Updated Travel Locations"

            updated_ranking = repository.update_ranking(
                ranking.id,
                title=new_title,
                description=None
            )

            assert updated_ranking is not None
            assert updated_ranking.title == new_title
            assert updated_ranking.description == ""

            db_ranking = RankingList.objects.get(id=ranking.id)
            assert db_ranking.title == new_title
            assert db_ranking.description == ""

        def test_update_non_existent_ranking(self, repository):
            non_existent_id = 999

            updated_ranking = repository.update_ranking(
                non_existent_id,
                "New Title",
                "New Description"
            )

            assert updated_ranking is None


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