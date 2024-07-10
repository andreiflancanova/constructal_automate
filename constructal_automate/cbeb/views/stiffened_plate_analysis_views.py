from cbeb.services.stiffened_plate_analysis_service import StiffenedPlateAnalysisService
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from cbeb.models import StiffenedPlateAnalysis
from cbeb.serializers import StiffenedPlateAnalysisSerializer


ROOT_DIR_COMPLETE_PATH = 'D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_analysis_files'

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
        return Response(service.validate_mapdl_connection(ROOT_DIR_COMPLETE_PATH, 'TEST2'))