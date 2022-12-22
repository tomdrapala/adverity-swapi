from rest_framework import views, generics

from people.models import Character
from people.serializers import CharacterSerializer
from people.utils import get_people


class CharacterView(generics.ListAPIView):
    serializer_class = CharacterSerializer
    queryset = Character.objects.all()

    def get(self, request, *args, **kwargs):
        data = get_people()
        return super().get(request, *args, **kwargs)
