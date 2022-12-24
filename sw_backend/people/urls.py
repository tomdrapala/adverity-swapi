from django.urls import path

from people.views import CharacterView, FetchPeopleDataView


urlpatterns = [
    path('', CharacterView.as_view(), name='character_list_view'),
    path('fetch_people_data/', FetchPeopleDataView.as_view(), name='fetch_people_data_view'),
]
