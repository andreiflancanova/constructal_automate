from rest_framework import status, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from csg.models import StiffenedPlate
from csg.serializers import StiffenedPlateSerializer


class StiffenedPlateViewSet(viewsets.ModelViewSet):
    def list(self, request):
        queryset = StiffenedPlate.objects.all()
        serializer = StiffenedPlateSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = StiffenedPlate.objects.all()
        plate = get_object_or_404(queryset, pk=pk)
        serializer = StiffenedPlateSerializer(plate)
        return Response(serializer.data)

    def create(self, request):
        print(request.data)
        serializer = StiffenedPlateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, pk=None, *args, **kwargs):
        instance = self.get_object(pk)
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