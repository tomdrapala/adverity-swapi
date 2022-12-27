from django.urls import path, include
from rest_framework import routers

from people.views import FetchPeopleDataView
from people.viewsets import PeopleViewSet

user_router = routers.SimpleRouter()
user_router.register(r'', PeopleViewSet, basename='people_viewset')


urlpatterns = [
    path('fetch_people_data/', FetchPeopleDataView.as_view(), name='fetch_people_data_view'),
    path('', include(user_router.urls)),
]
