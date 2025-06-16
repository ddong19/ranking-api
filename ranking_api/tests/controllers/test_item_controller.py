import json
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock
from ranking_api.services import RankingService, ItemService
from ranking_api.models import Item, RankingList


@patch.object(RankingService, 'get_ranking')
@patch.object(ItemService, 'get_all_items')
class TestGetAllRankingItems(TestCase):

    def test_get_ranking_items_success(self, mock_get_all_items, mock_get_ranking):
        ranking_id = 1
        mock_get_ranking.return_value = MagicMock()
        mock_get_all_items.return_value = []

        response = self.client.get(reverse('ranking-items', kwargs={'ranking_id': ranking_id}))

        self.assertEqual(response.status_code, 200)
        mock_get_ranking.assert_called_once_with(ranking_id)
        mock_get_all_items.assert_called_once_with(ranking_id)


    def test_get_ranking_items_empty(self, mock_get_all_items, mock_get_ranking):
        ranking_id = 1
        mock_get_ranking.return_value = MagicMock()
        mock_get_all_items.return_value = []

        response = self.client.get(reverse('ranking-items', kwargs={'ranking_id': ranking_id}))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['items'], [])
        mock_get_all_items.assert_called_once_with(ranking_id)


    def test_get_ranking_items_ranking_not_found(self, mock_get_item, mock_get_ranking):
        ranking_id = 100
        mock_get_ranking.return_value = None

        response = self.client.get(reverse('ranking-items', kwargs={'ranking_id': ranking_id}))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'{"error": "Ranking not found"}')
        mock_get_ranking.assert_called_once_with(ranking_id)

@patch.object(RankingService, 'get_ranking')
@patch.object(ItemService, 'get_item')
class TestGetRankingItem(TestCase):
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
            'item_id': item_id
        }))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['name'], 'London')
        self.assertEqual(data['notes'], 'some notes')
        mock_get_item.assert_called_once_with(item_id)


    def test_get_item_no_notes_success(self, mock_get_item, mock_get_ranking):
        ranking_id = 1
        item_id = 1
        mock_get_ranking.return_value = MagicMock()
        mock_item = MagicMock()
        mock_item.id = item_id
        mock_item.name = 'London'
        mock_item.notes = ""
        mock_item.rank = 1
        mock_item.ranking.id = ranking_id
        mock_get_item.return_value = mock_item

        response = self.client.get(reverse('ranking-item', kwargs={
            'item_id': item_id
        }))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['name'], 'London')
        mock_get_item.assert_called_once_with(item_id)


    def test_get_item_not_found(self, mock_get_item, mock_get_ranking):
        item_id = 100
        mock_get_ranking.return_value = MagicMock()
        mock_get_item.return_value = None

        response = self.client.get(reverse('ranking-item', kwargs={
            'item_id': item_id
        }))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'{"error": "Item not found"}')
        mock_get_item.assert_called_once_with(item_id)

@patch.object(ItemService, 'create_item')
class TestCreateRankingItem(TestCase):
    # success
    def test_create_item_success(self, mock_create_item):
        ranking = RankingList.objects.create(title='London')
        expected_item = Item(name="London", notes="some notes", rank=1, ranking_id=ranking.id)
        mock_create_item.return_value = expected_item

        response = self.client.post(
            reverse('ranking-items', kwargs={'ranking_id': ranking.id}),
            data={
                'name': "London",
                'notes': "some notes",
            }
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            'name': 'London',
            'notes': 'some notes',
            'rank': 1,
            'ranking_id': ranking.id
        })
    # no notes
    def test_create_item_no_notes_success(self, mock_create_item):
        ranking = RankingList.objects.create(title='Superheros')
        expected_item = Item(name="Batman", rank=1, ranking_id=ranking.id)
        mock_create_item.return_value = expected_item

        response = self.client.post(
            reverse('ranking-items', kwargs={'ranking_id': ranking.id}),
            data={
                'name': "Batman",
            }
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            'name': 'Batman',
            'notes': None,
            'rank': 1,
            'ranking_id': ranking.id
        })
    # no name error
    def test_create_item_missing_name(self, mock_create_item):
        ranking = RankingList.objects.create(title='Cities')

        response = self.client.post(
            reverse('ranking-items', kwargs={'ranking_id': ranking.id}),
            data={
                'notes': "No name provided"
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'error': 'Name is required'
        })

        mock_create_item.assert_not_called()

    # database error
    def test_create_item_db_error(self, mock_create_item):
        ranking = RankingList.objects.create(title='Error Test')

        mock_create_item.side_effect = Exception('Database error occurred')

        response = self.client.post(
            reverse('ranking-items', kwargs={'ranking_id': ranking.id}),
            data={
                'name': "Broken Item",
                'notes': "Simulated DB failure"
            }
        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {
            'error': 'Database error occurred'
        })

        mock_create_item.assert_called_once_with(
            name='Broken Item',
            notes='Simulated DB failure',
            ranking_id=ranking.id,
            rank = None
        )

@patch.object(ItemService, 'delete_item')
class TestDeleteRankingItem(TestCase):
    def test_delete_item_success(self, mock_delete_item):
        item_id = 1

        response = self.client.delete(
            reverse('ranking-item', kwargs={'item_id': item_id}),
        )

        assert response.status_code == 200
        assert response.json() == {'success': True}
        mock_delete_item.assert_called_once_with(item_id)

    def test_delete_item_not_found(self, mock_delete_item):
        item_id = 999
        mock_delete_item.side_effect = Exception('Failed to delete item: DoesNotExist')

        response = self.client.delete(reverse('ranking-item', kwargs={'item_id': item_id}))

        assert response.status_code == 404
        assert response.json() == {'error': 'Failed to delete item: DoesNotExist'}
        mock_delete_item.assert_called_once_with(item_id)

@patch.object(ItemService, 'patch_item')
class TestPatchRankingItem(TestCase):
    def test_patch_item_success(self, mock_patch_item):
        item_id = 1
        ranking = RankingList.objects.create(title='Superheros')
        mock_item = Item(id=item_id, name='Updated Name', notes='Updated Notes', rank=2)
        mock_item.ranking = ranking
        mock_patch_item.return_value = mock_item

        request_data = {
            'name': 'Updated Name',
            'notes': 'Updated Notes'
        }

        response = self.client.patch(
            reverse('ranking-item', kwargs={'item_id': item_id}),
            data=request_data,
            content_type='application/json',
        )

        assert response.status_code == 200
        assert response.json() == {
            'id': item_id,
            'name': 'Updated Name',
            'notes': 'Updated Notes',
            'rank': 2,
            'ranking': ranking.id
        }
        mock_patch_item.assert_called_once_with(item_id, name='Updated Name', notes='Updated Notes')

    def test_patch_item_invalid_input(self, mock_patch_item):
        item_id = 1
        request_data = {}

        response = self.client.patch(
            reverse('ranking-item', kwargs={'item_id': item_id}),
            data=request_data,
            content_type='application/json',
        )

        assert response.status_code == 400
        assert response.json() == {'error': 'At least one of name or notes must be provided.'}
        mock_patch_item.assert_not_called()

    def test_patch_item_not_found(self, mock_patch_item):
        item_id = 999
        mock_patch_item.side_effect = Item.DoesNotExist("Item with id 999 not found.")

        request_data = {'name': 'Something New'}

        response = self.client.patch(
            reverse('ranking-item', kwargs={'item_id': item_id}),
            data=request_data,
            content_type='application/json',
        )

        assert response.status_code == 404
        assert response.json() == {'error': 'Item with id 999 not found.'}
        mock_patch_item.assert_called_once_with(item_id, name='Something New', notes=None)