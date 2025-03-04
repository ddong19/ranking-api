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
