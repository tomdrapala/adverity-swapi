from rest_framework import generics, views, status
from rest_framework.response import Response
from datetime import timedelta, datetime
from django.conf import settings

from people.models import Character, People
from people.serializers import CharacterSerializer, PeopleSerializer
from people.utils import refresh_characters, get_last_update_date, fetch_people_data


class CharacterView(generics.ListAPIView):
    serializer_class = CharacterSerializer
    queryset = Character.objects.all()

    def get(self, request, *args, **kwargs):
        # TODO: implement some safety mechanism if cache_table is not available
        # LAST_UPDATE is cached variable that holds information about time of last table update.
        # It has expiration date set to 3600 seconds - 1 hour.
        # If variable has expired it will be equal None.
        # Expiration time can be changed by 'TIMEOUT' value in CACHES settings.
        LAST_UPDATE = get_last_update_date()
        if not LAST_UPDATE:
            refresh_characters()
        return super().get(request, *args, **kwargs)


class FetchPeopleDataView(views.APIView):
    serializer_class = PeopleSerializer
    queryset = People.objects.all()

    def post(self, request, *args, **kwargs):
        data = fetch_people_data()
        # TODO: save fetched data into csv file and save it in People table
        # serializer = PeopleSerializer(data=data)
        return Response(status=status.HTTP_201_CREATED, data=data)
