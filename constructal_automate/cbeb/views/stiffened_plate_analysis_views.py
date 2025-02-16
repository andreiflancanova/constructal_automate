from rest_framework import status, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from cbeb.models import StiffenedPlateAnalysis
from cbeb.serializers import StiffenedPlateAnalysisSerializer
from cbeb.permissions import IsAuthenticatedForWriteMethods


class StiffenedPlateAnalysisViewSet(viewsets.ModelViewSet):

    queryset = StiffenedPlateAnalysis.objects.all()
    serializer_class = StiffenedPlateAnalysisSerializer
    permission_classes = [IsAuthenticatedForWriteMethods]

    def list(self, request):
        queryset = StiffenedPlateAnalysis.objects.all()
        serializer = StiffenedPlateAnalysisSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = StiffenedPlateAnalysis.objects.all()
        stiffened_plate_analysis = get_object_or_404(queryset, pk=pk)
        serializer = StiffenedPlateAnalysisSerializer(stiffened_plate_analysis)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()