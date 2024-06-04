from rest_framework import serializers
from django.shortcuts import get_object_or_404
from csg.models import Plate, StiffenedPlate
from csg.services import StiffenedPlateService


class StiffenedPlateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StiffenedPlate
        fields = '__all__'

    def create(self, validated_data):

        plate_id = validated_data.pop('plate').id
        print(plate_id)

        associated_plate = get_object_or_404(Plate, id=plate_id)

        a = associated_plate.a
        b = associated_plate.b
        t_0 = associated_plate.t_0

        phi = validated_data['phi']
        N_ls = validated_data['N_ls']
        N_ts = validated_data['N_ts']
        k = validated_data['k']

        service = StiffenedPlateService()
        h_s, t_s = service.calc_stiffener_dimensions(a, b, t_0, phi, N_ls, N_ts, k)

        t_1 = service.calc_corrected_plate_thickness(phi, t_0)

        validated_data['h_s'] = h_s
        validated_data['t_s'] = t_s
        validated_data['t_1'] = t_1

        stiffened_plate_instance = StiffenedPlate.objects.create(plate = associated_plate, **validated_data)

        return stiffened_plate_instance
