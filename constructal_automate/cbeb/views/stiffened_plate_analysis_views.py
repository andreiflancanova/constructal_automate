from cbeb.services.stiffened_plate_analysis_service import StiffenedPlateAnalysisService
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from cbeb.models import StiffenedPlateAnalysis
from cbeb.serializers import StiffenedPlateAnalysisSerializer


class StiffenedPlateAnalysisViewSet(viewsets.ModelViewSet):
    queryset = StiffenedPlateAnalysis.objects.all()
    
    def get_serializer_class(self):
        return StiffenedPlateAnalysisSerializer
    
    def retrieve(self, request, pk=None):
        queryset = StiffenedPlateAnalysis.objects.all()
        # stiffened_plate_analysis = get_object_or_404(queryset, pk=pk)
        # serializer = StiffenedPlateAnalysisSerializer(stiffened_plate_analysis)
        # return Response(serializer.data)
        service = StiffenedPlateAnalysisService()
        return Response(service.create_initial_analysis_files('teste-geracao-diretorio'))
    
    #TODO: Implement initial persistence for StiffenedPlateAnalysis entity