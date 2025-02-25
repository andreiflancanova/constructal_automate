from rest_framework import status, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from csg.models import Plate
from csg.serializers import PlateSerializer
from csg.permissions import IsAuthenticatedForWriteMethods

class PlateViewSet(viewsets.ModelViewSet):
    
    queryset = Plate.objects.all()
    permission_classes = [IsAuthenticatedForWriteMethods]
    
    def get_serializer_class(self):
        return PlateSerializer
    
    def list(self, request):
        queryset = Plate.objects.all()
        serializer = PlateSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Plate.objects.all()
        plate = get_object_or_404(queryset, pk=pk)
        serializer = PlateSerializer(plate)
        return Response(serializer.data)

    def create(self, request):
        serializer = PlateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        queryset = Plate.objects.all()
        plate = get_object_or_404(queryset, pk=pk)
        serializer = PlateSerializer(plate, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        queryset = Plate.objects.all()
        plate = get_object_or_404(queryset, pk=pk)
        plate.delete()
        return Response(status=204)