from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock
from ranking_api.services.ranking_service import RankingService
from ranking_api.models import RankingList


@patch.object(RankingService, 'get_all_rankings')
class TestGetAllRankingsEndpoint(TestCase):
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

    def test_get_all_rankings_empty(self, mock_get_all_rankings):
        mock_get_all_rankings.return_value = []

        response = self.client.get(reverse('rankings-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'rankings': []})
        mock_get_all_rankings.assert_called_once()

    def test_get_all_rankings_error(self, mock_get_all_rankings):
        mock_get_all_rankings.side_effect = Exception("Database error")

        response = self.client.get(reverse('rankings-list'))

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {'error': 'Database error'})
        mock_get_all_rankings.assert_called_once()


@patch.object(RankingService, 'get_ranking')
class TestGetRankingDetailEndpoint(TestCase):
    def test_get_ranking_success(self, mock_get_ranking):
        ranking_id = 1
        mock_ranking = MagicMock()
        mock_ranking.title = "Best Movies"
        mock_ranking.description = "Top movies of all time"
        mock_get_ranking.return_value = mock_ranking

        response = self.client.get(reverse('ranking-detail', kwargs={'ranking_id': ranking_id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'title': 'Best Movies',
            'description': 'Top movies of all time'
        })
        mock_get_ranking.assert_called_once_with(ranking_id)

    def test_get_ranking_not_found(self, mock_get_ranking):
        ranking_id = 999
        mock_get_ranking.return_value = None

        response = self.client.get(reverse('ranking-detail', kwargs={'ranking_id': ranking_id}))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error': 'Ranking not found'})
        mock_get_ranking.assert_called_once_with(ranking_id)

    def test_get_ranking_error(self, mock_get_ranking):
        ranking_id = 1
        mock_get_ranking.side_effect = Exception("Database error")

        response = self.client.get(reverse('ranking-detail', kwargs={'ranking_id': ranking_id}))

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {'error': 'Database error'})
        mock_get_ranking.assert_called_once_with(ranking_id)


@patch.object(RankingService, 'create_ranking')
class TestCreateRankingEndpoint(TestCase):
    def test_create_ranking_success(self, mock_create_ranking):
        expected_ranking = RankingList(title="Best Books", description="Must-read books")
        mock_create_ranking.return_value = expected_ranking

        response = self.client.post(reverse('rankings-list'), {
            'title': 'Best Books',
            'description': 'Must-read books'
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            'title': 'Best Books',
            'description': 'Must-read books'
        })
        mock_create_ranking.assert_called_once_with(
            title='Best Books',
            description='Must-read books'
        )

    def test_create_ranking_missing_description(self, mock_create_ranking):
        expected_ranking = RankingList(title="Best Books")
        mock_create_ranking.return_value = expected_ranking

        response = self.client.post(reverse('rankings-list'), {
            'title': 'Best Books',
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            'title': 'Best Books',
            'description': None
        })
        mock_create_ranking.assert_called_once_with(
            title='Best Books',
            description=None
        )

    def test_create_ranking_missing_title(self, mock_create_ranking):
        response = self.client.post(reverse('rankings-list'), {
            'description': 'Must-read books'
        })

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {
            'error': 'title is required'
        })
        mock_create_ranking.assert_not_called()

    def test_create_ranking_error(self, mock_create_ranking):
        mock_create_ranking.side_effect = Exception('Database error')

        response = self.client.post(reverse('rankings-list'), {
            'title': 'Best Books',
            'description': 'Must-read books'
        })

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {
            'error': 'Database error'
        })
        mock_create_ranking.assert_called_once_with(
            title='Best Books',
            description='Must-read books'
        )

@patch.object(RankingService, 'delete_ranking')
class TestDeleteRankingEndpoint(TestCase):
    def test_delete_ranking_success(self, mocker):
        ranking_id = 1
        response = self.client.delete(f'/api/rankings/{ranking_id}/')

        assert response.status_code == 200
        assert response.json() == {'success': True}
        mocker.assert_called_once_with(ranking_id)

    def test_delete_ranking_not_found(self, mocker):
        ranking_id = 999
        mocker.side_effect = Exception('Failed to delete ranking: DoesNotExist')

        response = self.client.delete(f'/api/rankings/{ranking_id}/')

        assert response.status_code == 404
        assert response.json() == {'error': 'Ranking not found'}
        mocker.assert_called_once_with(ranking_id)

    def test_delete_ranking_error(self, mocker):
        ranking_id = 1
        mocker.side_effect = Exception('Failed to delete ranking: Unexpected error')

        response = self.client.delete(f'/api/rankings/{ranking_id}/')

        assert response.status_code == 500
        assert response.json() == {'error': 'Failed to delete ranking: Unexpected error'}
        mocker.assert_called_once_with(ranking_id)

@patch.object(RankingService, 'update_ranking')
class TestUpdateRankingEndpoint(TestCase):
    def test_update_ranking_success(self, mocker):
        ranking_id = 1
        request_data = {
            'title': 'Updated Title',
            'description': 'Updated Description'
        }

        mock_ranking = MagicMock()
        mock_ranking.title = request_data['title']
        mock_ranking.description = request_data['description']
        mocker.return_value = mock_ranking

        response = self.client.put(
            f'/api/rankings/{ranking_id}/',
            data=request_data,
            content_type='application/json'
        )

        assert response.status_code == 200
        assert response.json() == {
            'title': request_data['title'],
            'description': request_data['description']
        }
        mocker.assert_called_once_with(1, 'Updated Title', 'Updated Description')

    def test_update_ranking_not_found(self, mocker):
        ranking_id = 999
        request_data = {
            'title': 'Updated Title',
            'description': 'Updated Description'
        }
        mocker.side_effect = Exception('Failed to update ranking: DoesNotExist')

        response = self.client.put(
            f'/api/rankings/{ranking_id}/',
            data=request_data,
            content_type='application/json'
        )

        assert response.status_code == 404
        assert response.json() == {'error': 'Ranking not found'}
        mocker.assert_called_once_with(999, 'Updated Title', 'Updated Description')

    def test_update_ranking_missing_title(self, mocker):
        ranking_id = 1
        request_data = {
            'description': 'Updated Description'
        }

        response = self.client.put(
            f'/api/rankings/{ranking_id}/',
            data=request_data,
            content_type='application/json'
        )

        assert response.status_code == 400
        assert response.json() == {'error': 'title is required'}
        mocker.assert_not_called()

    def test_update_ranking_error(self, mocker):
        ranking_id = 1
        request_data = {
            'title': 'Updated Title',
            'description': 'Updated Description'
        }
        mocker.side_effect = Exception('Failed to update ranking: Unexpected error')

        response = self.client.put(
            f'/api/rankings/{ranking_id}/',
            data=request_data,
            content_type='application/json'
        )

        assert response.status_code == 500
        assert response.json() == {'error': 'Failed to update ranking: Unexpected error'}
        mocker.assert_called_once_with(1, 'Updated Title', 'Updated Description')
