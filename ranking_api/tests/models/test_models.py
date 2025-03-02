import pytest

from ranking_api.models import RankingList, Item


class TestModels:
    @pytest.mark.django_db
    def test_ranking_list_str_representation(self, travel_ranking):
        assert str(travel_ranking) == "Travel Locations"


    @pytest.mark.django_db
    def test_item_str_representation(self, travel_item):
        assert str(travel_item) == "Chicago"


@pytest.fixture
def travel_ranking():
    return RankingList.objects.create(
        title="Travel Locations",
        description="The best places to visit",
    )


@pytest.fixture
def travel_item(travel_ranking):
    return Item.objects.create(
        ranking=travel_ranking,
        name="Chicago",
        rank=1
    )