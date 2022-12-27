import json

import petl as etl
from rest_framework import viewsets
from rest_framework.response import Response

from people import PEOPLE_CSV_PATH
from people.models import People
from people.serializers import PeopleSerializer


class PeopleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PeopleSerializer
    queryset = People.objects.existing()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        sink = etl.MemorySource()

        file_data = etl.fromcsv(f'{PEOPLE_CSV_PATH}/{instance.file_name}')
        start = int(request.query_params.get('start_row', 0))
        result = etl.dicts(file_data, start, start+10)
        result = etl.fromdicts(result)
        result.tojson(sink)
        return Response(json.loads(sink.getvalue()))
