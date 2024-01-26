from rest_framework import serializers
from .models import House

class HouseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ['name', 'description', 'address']

    def create(self, validated_data):
        user = self.context['request'].user
        house = House.objects.create(**validated_data)
        house.owner.set([user])
        return house


