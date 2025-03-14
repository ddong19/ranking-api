from ranking_api.models import RankingList
from typing import Optional

class RankingRepository:
    def __init__(self):
        self.model = RankingList

    def get_ranking(self, ranking_id) -> Optional[RankingList]:
        try:
            return self.model.objects.get(id=ranking_id)
        except self.model.DoesNotExist:
            return None

    def get_all_rankings(self) -> list[RankingList]:
        return list(self.model.objects.all())

    def create_ranking(self, title: str, description: str = None) -> RankingList:
        return self.model.objects.create(
            title=title,
            description=description if description is not None else ''
        )

    def delete_ranking(self, ranking_id: int) -> bool:
        try:
            ranking = self.model.objects.get(id=ranking_id)
            ranking.delete()
            return True
        except self.model.DoesNotExist:
            return False


