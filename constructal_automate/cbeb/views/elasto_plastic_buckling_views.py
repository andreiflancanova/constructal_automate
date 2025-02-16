from cbeb.models.elasto_plastic_buckling import ElastoPlasticBuckling
from cbeb.serializers.elasto_plastic_buckling_serializer import ElastoPlasticBucklingSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from cbeb.permissions import IsAuthenticatedForWriteMethods


class ElastoPlasticBucklingViewSet(viewsets.ModelViewSet):
    queryset = ElastoPlasticBuckling.objects.all()
    serializer_class = ElastoPlasticBucklingSerializer
    permission_classes = [IsAuthenticatedForWriteMethods]

    def list(self, request):
        queryset = ElastoPlasticBuckling.objects.all()
        serializer = ElastoPlasticBucklingSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = ElastoPlasticBuckling.objects.all()
        stiffened_plate = get_object_or_404(queryset, pk=pk)
        serializer = ElastoPlasticBucklingSerializer(stiffened_plate)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()
