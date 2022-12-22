from django.urls import path

from people.views import CharacterView


urlpatterns = [
    path('', CharacterView.as_view(), name='character_list_view'),
]
