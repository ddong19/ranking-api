from django.http import JsonResponse
from rest_framework import viewsets

from ranking_api.services.item_service import ItemService
from ranking_api.repositories.item_repository import ItemRepository
from ranking_api.repositories.ranking_repository import RankingRepository
from ranking_api.services.ranking_service import RankingService


class ItemController(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_service = ItemService(item_repository=ItemRepository())
        self.ranking_service = RankingService(ranking_repository=RankingRepository())


    def get_ranking_items(self, request, ranking_id: int):
        if self.ranking_service.get_ranking(ranking_id) is None:
            return JsonResponse({'error': 'Ranking not found'}, status=404)
        try:
            items = self.item_service.get_all_items(ranking_id)
            return JsonResponse({
                'items': [
                    {
                        'id': item.id,
                        'name': item.name,
                        'notes': item.notes,
                        'rank': item.rank,
                        'ranking_id': item.ranking.id
                    } for item in items
                ]
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


    def get_ranking_item(self, request, item_id: int):
        try:
            item = self.item_service.get_item(item_id)

            if item is None:
                return JsonResponse({'error': 'Item not found'}, status=404)

            return JsonResponse({
                'id': item.id,
                'name': item.name,
                'notes': item.notes,
                'rank': item.rank,
                'ranking_id': item.ranking.id
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def create_ranking_item(self, request, ranking_id: int):
        try:
            name = request.data.get('name')
            notes = request.data.get('notes')
            ranking_id = ranking_id

            if not name:
                return JsonResponse({'error': 'Name is required'}, status=400)

            item = self.item_service.create_item(
                name=name,
                notes=notes,
                ranking_id=ranking_id
            )

            return JsonResponse({
                'name': item.name,
                'notes': item.notes,
                'rank': item.rank,
                'ranking_id': item.ranking.id
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def delete_ranking_item(self, request, item_id: int):
        try:
            self.item_service.delete_item(item_id)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)