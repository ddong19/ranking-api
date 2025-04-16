import json
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock
from ranking_api.services import RankingService, ItemService


class TestItemController(TestCase):
    @patch.object(RankingService, 'get_ranking')
    @patch.object(ItemService, 'get_all_items')
    def test_get_ranking_items_success(self, mock_get_all_items, mock_get_ranking):
        ranking_id = 1
        mock_get_ranking.return_value = MagicMock()
        mock_get_all_items.return_value = []

        response = self.client.get(reverse('ranking-items', kwargs={'ranking_id': ranking_id}))

        self.assertEqual(response.status_code, 200)
        mock_get_ranking.assert_called_once_with(ranking_id)
        mock_get_all_items.assert_called_once_with(ranking_id)


    @patch.object(RankingService, 'get_ranking')
    @patch.object(ItemService, 'get_all_items')
    def test_get_ranking_items_empty(self, mock_get_all_items, mock_get_ranking):
        ranking_id = 1
        mock_get_ranking.return_value = MagicMock()
        mock_get_all_items.return_value = []

        response = self.client.get(reverse('ranking-items', kwargs={'ranking_id': ranking_id}))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['items'], [])
        mock_get_all_items.assert_called_once_with(ranking_id)


    @patch.object(RankingService, 'get_ranking')
    def test_get_ranking_items_ranking_not_found(self, mock_get_ranking):
        ranking_id = 100
        mock_get_ranking.return_value = None

        response = self.client.get(reverse('ranking-items', kwargs={'ranking_id': ranking_id}))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'{"error": "Ranking not found"}')
        mock_get_ranking.assert_called_once_with(ranking_id)


    @patch.object(RankingService, 'get_ranking')
    @patch.object(ItemService, 'get_item')
    def test_get_item_success(self, mock_get_item, mock_get_ranking):
        ranking_id = 1
        item_id = 1
        mock_get_ranking.return_value = MagicMock()
        mock_item = MagicMock()
        mock_item.id = item_id
        mock_item.name = 'London'
        mock_item.notes = "some notes"
        mock_item.rank = 1
        mock_item.ranking.id = ranking_id
        mock_get_item.return_value = mock_item

        response = self.client.get(reverse('ranking-item', kwargs={
            'ranking_id': ranking_id,
            'item_id': item_id
        }))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['name'], 'London')
        mock_get_item.assert_called_once_with(ranking_id, item_id)

    @patch.object(RankingService, 'get_ranking')
    @patch.object(ItemService, 'get_item')
    def test_get_item_no_notes_success(self, mock_get_item, mock_get_ranking):
        ranking_id = 1
        item_id = 1
        mock_get_ranking.return_value = MagicMock()
        mock_item = MagicMock()
        mock_item.id = item_id
        mock_item.name = 'London'
        mock_item.notes = None
        mock_item.rank = 1
        mock_item.ranking.id = ranking_id
        mock_get_item.return_value = mock_item

        response = self.client.get(reverse('ranking-item', kwargs={
            'ranking_id': ranking_id,
            'item_id': item_id
        }))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['name'], 'London')
        mock_get_item.assert_called_once_with(ranking_id, item_id)


    @patch.object(RankingService, 'get_ranking')
    @patch.object(ItemService, 'get_item')
    def test_get_item_not_found(self, mock_get_item, mock_get_ranking):
        ranking_id = 1
        item_id = 100
        mock_get_ranking.return_value = MagicMock()
        mock_get_item.return_value = None

        response = self.client.get(reverse('ranking-item', kwargs={
            'ranking_id': ranking_id,
            'item_id': item_id
        }))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'{"error": "Item not found"}')
        mock_get_item.assert_called_once_with(ranking_id, item_id)


    @patch.object(RankingService, 'get_ranking')
    def test_get_item_ranking_not_found(self, mock_get_ranking):
        ranking_id = 999
        item_id = 100
        mock_get_ranking.return_value = None

        response = self.client.get(reverse('ranking-item', kwargs={
            'ranking_id': ranking_id,
            'item_id': item_id
        }))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'{"error": "Ranking not found"}')
        mock_get_ranking.assert_called_once_with(ranking_id)
