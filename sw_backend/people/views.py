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
        INTERVAL = getattr(settings, 'UPDATE_INTERVAL', 0)
        LAST_UPDATE = get_last_update_date()
        if (not LAST_UPDATE or
            LAST_UPDATE and datetime.now()-LAST_UPDATE > timedelta(hours=INTERVAL)
        ):
            refresh_characters()
        return super().get(request, *args, **kwargs)
