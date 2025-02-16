from rest_framework import status, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from csg.models import StiffenedPlate
from csg.serializers import StiffenedPlateSerializer
from csg.permissions import IsAuthenticatedForWriteMethods


class StiffenedPlateViewSet(viewsets.ModelViewSet):
    
    queryset = StiffenedPlate.objects.all()
    permission_classes = [IsAuthenticatedForWriteMethods]
    
    def get_serializer_class(self):
        return StiffenedPlateSerializer
    
    def list(self, request):
        queryset = StiffenedPlate.objects.all()
        serializer = StiffenedPlateSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = StiffenedPlate.objects.all()
        stiffened_plate = get_object_or_404(queryset, pk=pk)
        serializer = StiffenedPlateSerializer(stiffened_plate)
        return Response(serializer.data)

    def create(self, request):
        serializer = StiffenedPlateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = StiffenedPlate.objects.all()
        my_model = get_object_or_404(queryset, pk=pk)
        my_model.delete()
        return Response(status=204)