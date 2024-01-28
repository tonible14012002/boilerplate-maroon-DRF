from rest_framework import serializers
from rest_framework.fields import empty
from core_apps.user import serializers as user_serializers
from django.contrib.auth import get_user_model
from mixin import serializers as mixin_serializers
from . import models

User = get_user_model()


class RHouseBasic(serializers.ModelSerializer):
    pass

    class Meta:
        model = models.House
        fields = ["id", "name"]


class CRURoomDetail(
    serializers.ModelSerializer, mixin_serializers.NoUpdateSerializer
):
    # NOTE: `house_id` field is only required when creating a new room
    # Updating existed room doesn't require `house_id` field
    house = RHouseBasic(read_only=True)
    house_id = serializers.UUIDField(write_only=True, required=True)

    class Meta:
        model = models.Room
        fields = ["id", "name", "description", "house", "house_id"]
        extra_kwargs = {
            "description": {"required": False},
        }
        no_update_fields = ["house_id"]

    def update(self, instance, validated_data):
        room = instance
        return room.update(
            name=validated_data.get("name", None),
            description=validated_data.get("description", None),
        )

    def create(self, validated_data):
        house_id = validated_data.pop("house_id", None)
        try:
            house = models.House.objects.get(id=house_id)
            return models.Room.create_new(
                name=validated_data.get("name", ""),
                description=validated_data.get("description", ""),
                house=house,
            )
        except models.House.DoesNotExist:
            raise serializers.ValidationError("House not found")


class CHouseFromHouse(serializers.ModelSerializer):
    """
    This Serializer is for used nested in HouseSerializer
    for create room with house at the same time.
    Otherwise, use `CRURoomDetail` instead.c
    """

    class Meta:
        model = models.House
        fields = ["id", "name", "description", "address"]


class CRUHouseDetail(serializers.ModelSerializer):
    # NOTE: Read house owners use this field
    owners = user_serializers.ReadBasicUserProfile(many=True, read_only=True)
    # NOTE: Set house owners use this field
    owner_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=True
    )
    rooms = CHouseFromHouse(many=True)

    class Meta:
        model = models.House
        fields = [
            "id",
            "name",
            "description",
            "address",
            "owners",
            "owner_ids",
            "rooms",
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
        if not len(owners):
            raise serializers.ValidationError("User not found")
        house = models.House.create_new(
            owners=[owners],
            name=validated_data.get("name", ""),
            description=validated_data.get("description", ""),
            address=validated_data.get("address", ""),
        )

        rooms_data = validated_data.pop("rooms", [])
        for data in rooms_data:
            models.Room.create_new(
                house=house,
                name=data.get("name", ""),
                description=data.get("description", ""),
            )

        return house
