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

        t_1 = service.calc_corrected_plate_thickness(phi, t_0, k)

        validated_data['h_s'] = h_s
        validated_data['t_s'] = t_s
        validated_data['t_1'] = t_1

        stiffened_plate_instance = StiffenedPlate.objects.create(plate = associated_plate, **validated_data)

        return stiffened_plate_instance

    def update(self, instance, validated_data):
        plate_id = validated_data.pop('plate').id
        associated_plate = get_object_or_404(Plate, id=plate_id)

        a = associated_plate.a
        b = associated_plate.b
        t_0 = associated_plate.t_0

        phi = validated_data.get('phi', instance.phi)
        N_ls = validated_data.get('N_ls', instance.N_ls)
        N_ts = validated_data.get('N_ts', instance.N_ts)
        k = validated_data.get('k', instance.k)

        service = StiffenedPlateService()
        h_s, t_s = service.calc_stiffener_dimensions(a, b, t_0, phi, N_ls, N_ts, k)
        t_1 = service.calc_corrected_plate_thickness(phi, t_0, k)

        instance.plate = associated_plate
        instance.phi = phi
        instance.N_ls = N_ls
        instance.N_ts = N_ts
        instance.k = k
        instance.h_s = h_s
        instance.t_s = t_s
        instance.t_1 = t_1

        instance.save()
        return instance