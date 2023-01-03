"""sw_backend URL Configuration"""
from django.urls import path, re_path, include
from django.conf import settings

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from people.urls import api_people_urlpatterns, people_urlpatterns


urlpatterns = [
    path('', include(people_urlpatterns)),
    path('api/', include(api_people_urlpatterns)),
]

# Swagger DOCS
if settings.DEBUG:
    schema_view = get_schema_view(
        openapi.Info(
            title="SW API",
            default_version='v1',
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )
    urlpatterns.extend([
        re_path(r'^docs/$',
                schema_view.with_ui('swagger', cache_timeout=0),
                name='schema-swagger-ui')])
