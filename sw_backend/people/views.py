import csv
import json
from datetime import datetime

import petl as etl
from django.views.generic.base import TemplateView
from rest_framework import status, views
from rest_framework.response import Response

from people import PEOPLE_CSV_PATH
from people.models import People
from people.serializers import PeopleSerializer
from people.utils import fetch_people_data


class EntryView(TemplateView):
    template_name = 'people/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = People.objects.existing()
        serializer = PeopleSerializer(queryset, many=True)
        context['people_data'] = json.dumps(serializer.data)
        # context['people_data'] = []
        return context


# class CharacterAPIView(generics.ListAPIView):
#     serializer_class = CharacterSerializer
#     queryset = Character.objects.all()

#     def get(self, request, *args, **kwargs):
#         # TODO: implement some safety mechanism if cache_table is not available
#         # LAST_UPDATE is cached variable that holds information about time of last table update.
#         # It has expiration date set to 3600 seconds - 1 hour.
#         # If variable has expired it will be equal None.
#         # Expiration time can be changed by 'TIMEOUT' value in CACHES settings.
#         LAST_UPDATE = get_last_update_date()
#         if not LAST_UPDATE:
#             refresh_characters()
#         return super().get(request, *args, **kwargs)


class FetchPeopleAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        characters_data = fetch_people_data()
        name = f'{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.csv'
        file_path = f'{PEOPLE_CSV_PATH}/{name}'

        # table = [[field for field in characters_data[0]]]
        # etl.tocsv(table, file_path)
        # for row in characters_data:
        #     etl.io.csv.appendcsv([value for value in row.values()], file_path)
        with open(file_path, 'w') as file:
            writer = csv.writer(file)
            writer.writerow([field for field in characters_data[0]])
            for row in characters_data:
                writer.writerow([value for value in row.values()])
        data = {'file_name': name}
        serializer = PeopleSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=data)
