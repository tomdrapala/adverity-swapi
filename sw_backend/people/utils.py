import json
import requests
import threading
from datetime import datetime

from django.conf import settings
from django.core.cache import cache
from rest_framework import status

from people.serializers import CharacterSerializer
from people.models import Character

PEOPLE_URL = getattr(settings, 'PEOPLE_URL', '')
HOMEWORLD_URL = getattr(settings, 'HOMEWORLD_URL', '')


update_lock = threading.Lock()


def get_last_update_date():
    return cache.get('CHARACTER_LAST_UPDATE_DATE')


def update_last_update_date():
    with update_lock:
        cache.set('CHARACTER_LAST_UPDATE_DATE', datetime.now())


def fetch_data(url):
    # url = 'https://www.google.com'
    result = requests.get(url)
    if getattr(result, 'status_code', 0) == status.HTTP_200_OK:
        try:
            return json.loads(result.content)
        except json.JSONDecodeError:
            # TODO: set up logger
            pass
    return dict()


def get_resource_data(url):
    # To decrease waiting time of data fetch we could for example
    # send requests in multiple threads or processes
    data = list()
    chunk = fetch_data(url)
    data.extend(chunk.get('results', []))
    while chunk.get('next'):
        chunk = fetch_data(chunk['next'])
        data.extend(chunk.get('results'))
    # with open('local/people.json', 'r') as file:
    #     data = json.load(file)
    return data


def get_homeworld_mapping(homeworld_data):
    mapping = dict()
    for url in homeworld_data:
        planet_id = url.split('/')[-2]
        if planet_id not in mapping:
            planet = fetch_data(url)
            if name := planet.get('name'):
                mapping[planet_id] = name

    # Alternative version
    # homeworld_data = get_resource_data(HOMEWORLD_URL)
    # mapping = dict()
    # for obj in homeworld_data:
    #     planet_id = obj['url'].split('/')[-2]
    #     mapping[planet_id] = obj['name']

    # with open('local/planet_mapping.json', 'r') as file:
    #     mapping = json.load(file)
    return mapping


def substitute_homeworld_names(data):
    homeworlds = {obj.get('homeworld') for obj in data}
    homeworld_mapping = get_homeworld_mapping(homeworlds)
    for obj in data:
        planet_id = obj['homeworld'].split('/')[-2]
        obj['homeworld'] = homeworld_mapping[planet_id]
    return data


def refresh_characters():
    data = get_resource_data(PEOPLE_URL)
    data = substitute_homeworld_names(data)
    if data:
        serializer = CharacterSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        # After validation we can safely clean Character records
        # knowing that they will be replaced by freshly fetched data
        Character.objects.all().delete()
        serializer.save()
        update_last_update_date()


def fetch_people_data():
    data = get_resource_data(PEOPLE_URL)
    data = substitute_homeworld_names(data)
    if data:
        serializer = CharacterSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data
