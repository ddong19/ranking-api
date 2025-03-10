from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock
from ranking_api.services.ranking_service import RankingService


class TestRankingController(TestCase):
    @patch.object(RankingService, 'get_all_rankings')
    def test_get_all_rankings_success(self, mock_get_all_rankings):
        mock_ranking1 = MagicMock()
        mock_ranking1.title = "Best Movies"
        mock_ranking1.description = "Top movies of all time"

        mock_ranking2 = MagicMock()
        mock_ranking2.title = "Best Books"
        mock_ranking2.description = "Must-read books"

        mock_get_all_rankings.return_value = [mock_ranking1, mock_ranking2]

        response = self.client.get(reverse('rankings-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'rankings': [
                {
                    'title': 'Best Movies',
                    'description': 'Top movies of all time'
                },
                {
                    'title': 'Best Books',
                    'description': 'Must-read books'
                }
            ]
        })
        mock_get_all_rankings.assert_called_once()


    @patch.object(RankingService, 'get_all_rankings')
    def test_get_all_rankings_empty(self, mock_get_all_rankings):
        mock_get_all_rankings.return_value = []

        response = self.client.get(reverse('rankings-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'rankings': []})
        mock_get_all_rankings.assert_called_once()


    @patch.object(RankingService, 'get_all_rankings')
    def test_get_all_rankings_error(self, mock_get_all_rankings):
        mock_get_all_rankings.side_effect = Exception("Database error")

        response = self.client.get(reverse('rankings-list'))

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {'error': 'Database error'})
        mock_get_all_rankings.assert_called_once()


    @patch.object(RankingService, 'get_ranking')
    def test_get_ranking_success(self, mock_get_ranking):
        # Arrange
        ranking_id = 1
        mock_ranking = MagicMock()
        mock_ranking.title = "Best Movies"
        mock_ranking.description = "Top movies of all time"
        mock_get_ranking.return_value = mock_ranking

        # Act
        response = self.client.get(reverse('ranking-detail', kwargs={'ranking_id': ranking_id}))

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'title': 'Best Movies',
            'description': 'Top movies of all time'
        })
        mock_get_ranking.assert_called_once_with(ranking_id)

    @patch.object(RankingService, 'get_ranking')
    def test_get_ranking_not_found(self, mock_get_ranking):
        # Arrange
        ranking_id = 999
        mock_get_ranking.return_value = None

        # Act
        response = self.client.get(reverse('ranking-detail', kwargs={'ranking_id': ranking_id}))

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error': 'Ranking not found'})
        mock_get_ranking.assert_called_once_with(ranking_id)

    @patch.object(RankingService, 'get_ranking')
    def test_get_ranking_error(self, mock_get_ranking):
        # Arrange
        ranking_id = 1
        mock_get_ranking.side_effect = Exception("Database error")

        # Act
        response = self.client.get(reverse('ranking-detail', kwargs={'ranking_id': ranking_id}))

        # Assert
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {'error': 'Database error'})
        mock_get_ranking.assert_called_once_with(ranking_id)

