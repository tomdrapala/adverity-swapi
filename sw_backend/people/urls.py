from django.urls import path, include
from rest_framework import routers

from people.views import FetchPeopleAPIView, EntryView
from people.viewsets import PeopleAPIViewSet

router = routers.SimpleRouter()
router.register(r'', PeopleAPIViewSet, basename='people_viewset')


people_urlpatterns = [
    path('', EntryView.as_view(), name='entry_view'),
]


api_people_urlpatterns = [
    path('fetch_data/', FetchPeopleAPIView.as_view(), name='fetch_people_data_view'),
    path('', include(router.urls)),
]
