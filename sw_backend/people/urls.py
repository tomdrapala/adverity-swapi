from django.urls import path, include
from rest_framework import routers

from people.views import FetchPeopleAPIView, PeopleListView, PeopleDetailView
from people.viewsets import PeopleAPIViewSet

router = routers.SimpleRouter()
router.register(r'', PeopleAPIViewSet, basename='people_viewset')


people_urlpatterns = [
    path('', PeopleListView.as_view(), name='people_list'),
    path('<int:id>/', PeopleDetailView.as_view(), name='people_detail'),
]


api_people_urlpatterns = [
    path('fetch_people_data/', FetchPeopleAPIView.as_view(), name='fetch_people_data_view'),
    path('people/', include(router.urls)),
]
