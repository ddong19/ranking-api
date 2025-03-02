from django.http import JsonResponse
from rest_framework import viewsets
from typing import Optional

from ranking_api.services.item_service import ItemService
from ranking_api.repositories.item_repository import ItemRepository


class ItemController(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_service = ItemService(item_repository=ItemRepository())

    def get_ranking_items(self, request, ranking_id: int):
        try:
            items = self.item_service.get_items(ranking_id)
            return JsonResponse({
                'items': [
                    {
                        'id': item.id,
                        'name': item.name,
                        'rank': item.rank,
                        'ranking_id': item.ranking.id
                    } for item in items
                ]
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

