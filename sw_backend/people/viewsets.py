import json

import petl as etl
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from people import PEOPLE_CSV_PATH
from people.models import People
from people.serializers import PeopleSerializer


class PeopleAPIViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PeopleSerializer
    queryset = People.objects.existing().order_by('-id')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        sink = etl.MemorySource()

        file_data = etl.fromcsv(f'{PEOPLE_CSV_PATH}/{instance.file_name}')
        start = int(request.query_params.get('start_row', 0))
        result = etl.dicts(file_data, start, start+10)
        result = etl.fromdicts(result)
        try:
            result.tojson(sink)
        except FileNotFoundError:
            # TODO: set up logger
            # We could set up some email notifications to inform of such situation
            instance.is_removed = True
            instance.save()
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(json.loads(sink.getvalue()))

    @action(methods=['GET'], detail=True, url_path='file_name')
    def get_file_name(self, request, **kwargs):
        """Return the file name"""
        file_name = People.objects.filter(id=96).values_list('file_name').first()
        if file_name:
            return Response({"file_name": file_name[0]})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['GET'], detail=True, url_path='value_count')
    def get_value_count(self, request, **kwargs):
        """Return the file name"""
        columns = request.query_params.get('columns', '').split(',')
        instance = self.get_object()
        sink = etl.MemorySource()
        file_data = etl.fromcsv(f'{PEOPLE_CSV_PATH}/{instance.file_name}')
        table = etl.cut(file_data, *columns)
        table = etl.aggregate(table, (columns), len)
        result = etl.dicts(table)
        result = etl.fromdicts(result)
        try:
            result.tojson(sink)
        except FileNotFoundError:
            instance.is_removed = True
            instance.save()
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(json.loads(sink.getvalue()))
