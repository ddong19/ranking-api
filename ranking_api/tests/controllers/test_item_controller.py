import json
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from ranking_api.models import RankingList, Item

class TestItemController(TestCase):
    def setUp(self):
        self.client = Client()

        # Create test data
        self.ranking = RankingList.objects.create(
            title="Travel Locations",
            description="The best places to visit",
        )

        self.empty_ranking = RankingList.objects.create(
            title="Empty",
            description="No items",
        )

        self.items = [
            Item.objects.create(
                ranking=self.ranking,
                name="London",
                notes="The capital of England",
                rank=1
            ),
            Item.objects.create(
                ranking=self.ranking,
                name="Paris",
                notes = "The capital of France",
                rank=2
            )
        ]

        # Create test URLs
        self.ranking_items_url = reverse(
            'ranking-items',
            kwargs={'ranking_id': self.ranking.id}
        )

        self.ranking_item_url = reverse(
            'ranking-item',
            kwargs={'ranking_id': self.ranking.id, 'item_id': self.items[0].id}
        )

    @patch('ranking_api.services.ItemService')
    def test_get_ranking_items(self, mock_service):
        mock_service.get_all_items.return_value = self.items

        response = self.client.get(self.ranking_items_url)

        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual(len(data['items']), 2)
        self.assertEqual(data['items'][0]['name'], 'London')
        self.assertEqual(data['items'][1]['name'], 'Paris')


    @patch('ranking_api.services.ItemService')
    def test_get_ranking_items_empty(self, mock_service):
        mock_service.get_all_items.return_value = []

        url = reverse('ranking-items', kwargs={'ranking_id': self.empty_ranking.id})

        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual(data['items'], [])

    @patch('ranking_api.services.ItemService')
    def test_get_ranking_items_ranking_not_found(self, mock_service):
        mock_service.get_all_items.return_value = None

        url = reverse('ranking-items', kwargs={'ranking_id': 100})

        response = self.client.get(url)
        self.assertEqual(404, response.status_code)
        self.assertEqual(response.content, b'{"error": "Ranking not found"}')

    #TODO: test return 404 if ranking_id doesn't exist


    @patch('ranking_api.services.ItemService')
    def test_get_ranking_item(self, mock_service):
        mock_service.get_item.return_value = self.items[0]

        response = self.client.get(self.ranking_item_url)

        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual('London', data['name'])


    @patch('ranking_api.services.ItemService')
    def test_get_ranking_item_not_found(self, mock_service):
        mock_service.get_item.return_value = None

        url = reverse('ranking-item', kwargs={'ranking_id': self.empty_ranking.id, 'item_id': 100})

        response = self.client.get(url)

        self.assertEqual(404, response.status_code)
        self.assertEqual(response.content, b'{"error": "Item not found"}')

    @patch('ranking_api.services.ItemService')
    def test_get_ranking_ranking_not_found(self, mock_service):
        mock_service.get_item.return_value = None

        url = reverse('ranking-item', kwargs={'ranking_id': 999, 'item_id': 100})

        response = self.client.get(url)

        self.assertEqual(404, response.status_code)
        self.assertEqual(response.content, b'{"error": "Ranking not found"}')


