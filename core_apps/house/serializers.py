from rest_framework import serializers
from core_apps.user import serializers as user_serializers
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()


class CRUHouseDetail(serializers.ModelSerializer):
    # NOTE: Read house owners use this field
    owners = user_serializers.ReadBasicUserProfile(many=True, read_only=True)
    # NOTE: Set house owners use this field
    owner_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=True
    )

    class Meta:
        model = models.House
        fields = [
            "id",
            "name",
            "description",
            "address",
            "owners",
            "owner_ids",
        ]
        extra_kwargs = {
            "description": {"required": False},
            "address": {"required": False},
        }

    def validate_owner_ids(self, value):
        if not len(value):
            raise serializers.ValidationError("At least one owner is required")
        return value

    def update(self, instance, validated_data):
        house = instance
        owner_ids = validated_data.pop("owner_ids", [])
        if owner_ids:
            house.owners.set(User.objects.from_ids(*owner_ids))
        return house.update(
            name=validated_data.get("name", None),
            description=validated_data.get("description", None),
            address=validated_data.get("address", None),
        )

    def create(self, validated_data):
        owner_ids = validated_data.pop("owner_ids", [])
        owners = []
        if owner_ids:
            owners = User.objects.from_ids(*owner_ids)
        return models.House.create_new(
            owners=[owners],
            name=validated_data["name"],
            description=validated_data["description"],
            address=validated_data["address"],
        )
