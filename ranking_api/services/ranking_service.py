from ranking_api.repositories.ranking_repository import RankingRepository
from ranking_api.models import RankingList
from typing import Optional


class RankingService:
    def __init__(self, ranking_repository: RankingRepository):
        self.ranking_repository = ranking_repository

    def get_ranking(self, ranking_id: int) -> Optional[RankingList]:
        return self.ranking_repository.get_ranking(ranking_id)

    def get_all_rankings(self) -> list[RankingList]:
        return self.ranking_repository.get_all_rankings()