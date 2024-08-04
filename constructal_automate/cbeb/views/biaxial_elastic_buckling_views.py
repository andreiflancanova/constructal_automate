from cbeb.models.biaxial_elastic_buckling import BiaxialElasticBuckling
from cbeb.serializers.biaxial_elastic_buckling_serializer import BiaxialElasticBucklingSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class BiaxialElasticBucklingViewSet(viewsets.ModelViewSet):
    queryset = BiaxialElasticBuckling.objects.all()
    serializer_class = BiaxialElasticBucklingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()