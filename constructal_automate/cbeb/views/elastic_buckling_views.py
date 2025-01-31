from cbeb.models.elastic_buckling import ElasticBuckling
from cbeb.serializers.elastic_buckling_serializer import ElasticBucklingSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class ElasticBucklingViewSet(viewsets.ModelViewSet):
    queryset = ElasticBuckling.objects.all()
    serializer_class = ElasticBucklingSerializer

    def list(self, request):
        queryset = ElasticBuckling.objects.all()
        serializer = ElasticBucklingSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = ElasticBuckling.objects.all()
        stiffened_plate = get_object_or_404(queryset, pk=pk)
        serializer = ElasticBucklingSerializer(stiffened_plate)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()
