from rest_framework import status, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from csg.models import Plate
from csg.serializers import PlateSerializer


class PlateViewSet(viewsets.ModelViewSet):
    
    queryset = Plate.objects.all()
    
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
        my_model = get_object_or_404(queryset, pk=pk)
        my_model.delete()
        return Response(status=204)