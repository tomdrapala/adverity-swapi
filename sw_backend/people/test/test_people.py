import json
import os
from unittest.mock import patch
import petl as etl

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from people import PEOPLE_CSV_PATH
from people.models import People
from people.utils import substitute_homeworld_names


class PeopleTestCase(TestCase):
    fixtures = ['people/test/fixtures/people.json']

    def setUp(self):
        self.client = APIClient()
        self.url_fetch = reverse('fetch_people_data_view')
        self.url_list = reverse('people_viewset-list')
        self.url_detail = reverse('people_viewset-detail', args=('1'))
        self.csv_filename = '2023-01-01_01-01-01.csv'
        self.input_data_path = os.path.join(os.path.dirname(__file__), 'test_data')
        self.people_data_path = os.path.join(self.input_data_path, 'people_data.json')
        self.raw_people_data_path = os.path.join(self.input_data_path, 'people_data_raw.json')

    @patch('people.utils.get_homeworld_mapping')
    @patch('people.utils.get_resource_data')
    def test_swapi_is_fetched(self, mock_people, mock_homeworld):
        """Test that swapi requests are sent"""
        self.client.post(self.url_fetch)
        mock_people.assert_called()
        mock_homeworld.assert_called()

    @patch('people.utils.get_resource_data')
    def test_homeworld_name_substitution(self, mock_fetch):
        """Test that homeworld urls are correctly replaced with names"""
        mock_fetch.return_value = [
            {"url": "https://swapi.dev/api/planets/1/", "name": "Tatooine"},
            {"url": "https://swapi.dev/api/planets/2/", "name": "Alderaan"}
        ]
        with open(self.raw_people_data_path) as file:
            people_data = json.load(file)
        data = substitute_homeworld_names(people_data)
        for obj in data:
            # Required python version >= 3.10
            # match obj['name']:
            #     case 'Luke Skywalker':
            #         self.assertEqual(obj['homeworld'], 'Tatooine')
            #     case 'Leia Organa':
            #         self.assertEqual(obj['homeworld'], 'Alderaan')
            # Just in case, analogous logic but without match case
            if obj['name'] == 'Luke Skywalker':
                self.assertEqual(obj['homeworld'], 'Tatooine')
            elif obj['name'] == 'Leia Organa':
                self.assertEqual(obj['homeworld'], 'Alderaan')

    @patch('people.views.fetch_people_data')
    def test_csv_is_correctly_created_and_saved(self, mock_data):
        with open(self.people_data_path) as file:
            people_data = json.load(file)
        mock_data.return_value = people_data
        response = self.client.post(self.url_fetch)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        file_path = f"{PEOPLE_CSV_PATH}/{response.data['file_name']}"
        self.assertTrue(os.path.exists(file_path))

        data = etl.fromcsv(file_path)
        self.assertEqual(len(data.data()), len(people_data))
        input_names = {obj['name'] for obj in people_data}
        csv_names = {obj[0] for obj in data.data()}
        self.assertEqual(input_names, csv_names)

        os.remove(file_path)

    def test_user_can_list_people_data(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data_count = People.objects.existing().count()
        self.assertEqual(data_count, len(response.data))

    def test_objects_marked_as_removed_are_not_returned(self):
        response = self.client.get(self.url_list)
        removed = People.objects.filter(is_removed=True).first()
        for obj in response.data:
            self.assertNotEqual(obj['file_name'], removed.file_name)

    def test_cannot_post_to_people_list_endpoint(self):
        response = self.client.post(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_can_retrieve_people_details(self):
        """Endpoint returns 10 objects at a time, by default starting from first row of the csv data"""
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        file_path = f'{PEOPLE_CSV_PATH}/{self.csv_filename}'
        data = etl.fromcsv(file_path)

        self.assertEqual(len(response.data), 10)
        for i in range(10):
            self.assertEqual(data.data()[i][0], response.data[i]['name'])

    def test_can_retrieve_people_details_starting_from_specific_row(self):
        start_row = 20
        response = self.client.get(f'{self.url_detail}?start_row={start_row}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        file_path = f'{PEOPLE_CSV_PATH}/{self.csv_filename}'
        data = etl.fromcsv(file_path)
        data = etl.dicts(data, start_row, start_row+10)

        self.assertEqual(len(response.data), 10)
        for i in range(10):
            self.assertEqual(data[i]['name'], response.data[i]['name'])

    def test_can_retrieve_aggregated_data(self):
        columns = ['homeworld', 'gender']
        url = f'{self.url_detail}value_count/?columns={",".join(columns)}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        columns.append('value')
        for obj in response.data:
            self.assertEqual(list(obj.keys()), columns)
