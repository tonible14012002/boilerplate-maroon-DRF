from rest_framework import serializers
from .models import House
from core_apps.user.serializers import ReadUpdateUserProfile

class HouseDetailSerializer(serializers.ModelSerializer):
    owner = ReadUpdateUserProfile(many=True)
    class Meta:
        model = House
        fields = ['id', 'name', 'description', 'address', 'owner']

    def create(self, validated_data):
        user = self.context['request'].user
        house = House.objects.create(**validated_data)
        house.owner.set([user])
        return house

class UpdateHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ['id', 'name', 'description', 'address']

class DeleteHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ['id', 'name', 'description', 'address']