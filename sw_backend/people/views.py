from rest_framework import generics
from datetime import timedelta, datetime
from django.conf import settings

from people.models import Character
from people.serializers import CharacterSerializer
from people.utils import refresh_characters, get_last_update_date


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
