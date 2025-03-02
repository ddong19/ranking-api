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

    @patch('ranking_api.controllers.ItemController')
    def test_get_ranking_items(self, mock_controller):
        mock_controller.get_items.return_value = self.items

        response = self.client.get(self.ranking_items_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['items']), 2)
        self.assertEqual(data['items'][0]['name'], 'London')
        self.assertEqual(data['items'][1]['name'], 'Paris')