import csv
import random
import string
from datetime import datetime

from django.views.generic.base import TemplateView
from rest_framework import status, views
from rest_framework.response import Response

from people import PEOPLE_CSV_PATH
from people.serializers import PeopleSerializer
from people.utils import fetch_people_data


class PeopleListView(TemplateView):
    template_name = 'people/home.html'


class PeopleDetailView(TemplateView):
    template_name = 'people/detail.html'


class FetchPeopleAPIView(views.APIView):
    """Fetch current data from the [SWAPI](https://pipedream.com/apps/swapi) and save it in csv file."""
    def post(self, request, *args, **kwargs):
        characters_data = fetch_people_data()
        if characters_data:
            random_string = ''.join(random.choices(string.ascii_letters, k=7))
            name = f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_{random_string}.csv'
            file_path = f'{PEOPLE_CSV_PATH}/{name}'

            # I am writing 1 line at a time instead of creating a complete file in memory
            # and saving it at once, to avoid memory overflow.
            # In the current situation, it would be faster to generate a complete file,
            # because we are not fetching a big amount of data,
            # but it could become a problem if we'd be working with some bigger data source.
            with open(file_path, 'w') as file:
                writer = csv.writer(file)
                writer.writerow([field for field in characters_data[0]])
                for row in characters_data:
                    writer.writerow([value for value in row.values()])
            data = {'file_name': name}
            serializer = PeopleSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
