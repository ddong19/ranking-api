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

    def create_ranking(self, title: str, description: str = None) -> RankingList:
        return self.ranking_repository.create_ranking(title, description)

    def delete_ranking(self, ranking_id: int) -> None:
        deleted = self.ranking_repository.delete_ranking(ranking_id)
        if not deleted:
            raise RankingList.DoesNotExist(f"Ranking with id {ranking_id} does not exist.")

    def update_ranking(self, ranking_id: int, title: str, description: str = None) -> RankingList:
        updated_ranking = self.ranking_repository.update_ranking(ranking_id, title, description)
        if not updated_ranking:
            raise RankingList.DoesNotExist(f"Ranking with id {ranking_id} does not exist.")
        return updated_ranking


