from django.db import models
from ranking_api.models.ranking_list import RankingList

class Item(models.Model):
    name = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    rank = models.IntegerField()
    ranking_list = models.ForeignKey(RankingList, on_delete=models.CASCADE)

    def __str__(self):
        return self.name