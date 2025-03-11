from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from ranking_api.repositories.ranking_repository import RankingRepository
from ranking_api.services.ranking_service import RankingService

class RankingController(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ranking_service = RankingService(ranking_repository=RankingRepository())

    def get_all_rankings(self, request):
        try:
            rankings = self.ranking_service.get_all_rankings()
            return JsonResponse({
                'rankings': [
                    {
                        'title': ranking.title,
                        'description': ranking.description
                    } for ranking in rankings
                ]
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get_ranking(self, request, ranking_id: int):
        try:
            ranking = self.ranking_service.get_ranking(ranking_id)
            if ranking is None:
                return JsonResponse({'error': 'Ranking not found'}, status=404)
            return JsonResponse({
                'title': ranking.title,
                'description': ranking.description
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def create_ranking(self, request):
        try:
            title = request.data.get('title')
            description = request.data.get('description')

            if not title:
                return JsonResponse({'error': 'title is required'}, status=500)

            ranking = self.ranking_service.create_ranking(
                title=title,
                description=description
            )
            return JsonResponse({
                'title': ranking.title,
                'description': ranking.description
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)