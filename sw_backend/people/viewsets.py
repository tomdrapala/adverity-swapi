from logging import getLogger
import json

import petl as etl
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from people import PEOPLE_CSV_PATH
from people.models import People
from people.serializers import PeopleSerializer
logger = getLogger(__name__)


class PeopleAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """Return stored People data."""
    serializer_class = PeopleSerializer
    queryset = People.objects.existing().order_by('-id')

    def get_data(self, request, **kwargs):
        instance = get_object_or_404(People, pk=kwargs.get('pk'))
        file_data = etl.fromcsv(f'{PEOPLE_CSV_PATH}/{instance.file_name}')
        sink = etl.MemorySource()

        columns = request.query_params.get('columns')
        if self.action == 'get_value_count' and columns:
            columns = columns.split(',')
            table = etl.cut(file_data, *columns)
            table = etl.aggregate(table, (columns), len)
            result = etl.dicts(table)
        else:
            start_row = int(request.query_params.get('start_row', 0))
            result = etl.dicts(file_data, start_row, start_row+10)

        result = etl.fromdicts(result)
        try:
            result.tojson(sink)
        except FileNotFoundError:
            # We could set up email notifications to inform of such situation
            logger.error(f"Could not find CSV file - {instance}")
            instance.is_removed = True
            instance.save()
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(json.loads(sink.getvalue()))

    def retrieve(self, request, *args, **kwargs):
        return self.get_data(request, **kwargs)

    @action(methods=['GET'], detail=True, url_path='value_count')
    def get_value_count(self, request, **kwargs):
        """Return aggregated data for the column specified in the url `columns` parameter."""
        return self.get_data(request, **kwargs)

    @action(methods=['GET'], detail=True, url_path='file_name')
    def get_file_name(self, request, **kwargs):
        """Return the file name."""
        instance = get_object_or_404(People, pk=kwargs.get('pk'))
        return Response({"file_name": instance.file_name})

    @action(methods=['GET'], detail=True, url_path='file_download')
    def file_download(self, request, **kwargs):
        """Return csv file."""
        instance = get_object_or_404(People, pk=kwargs.get('pk'))
        with open(f'{PEOPLE_CSV_PATH}/{instance.file_name}', newline='') as csv_file:
            response = HttpResponse(csv_file, content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename={instance.file_name}'
            return response
