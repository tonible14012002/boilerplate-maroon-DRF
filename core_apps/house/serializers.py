from rest_framework import serializers
from core_apps.user import serializers as user_serializers
from core_apps.permission import models as permission_models
from django.contrib.auth import get_user_model
from mixin import serializers as mixin_serializers
from utils import list as list_utils
from . import models

User = get_user_model()


class CRURoomDetail(
    serializers.ModelSerializer, mixin_serializers.NoUpdateSerializer
):
    class RHouseBasic(serializers.ModelSerializer):
        class Meta:
            model = models.House
            fields = ["id", "name"]

    """
    CREATE: Required request context for grant room permission to request.user
    UPDATE: Update name, description fields only
    """
    # NOTE: `house_id` field is only required when creating a new room
    # Updating existed room doesn't require `house_id` field

    house = RHouseBasic(read_only=True)
    house_id = serializers.UUIDField(write_only=True)
    members = user_serializers.ReadBasicUserProfile(
        many=True, read_only=True, source="get_room_members"
    )
    allow_assign_member = serializers.SerializerMethodField(
        method_name="get_is_allow_assign_member"
    )

    class Meta:
        model = models.Room
        fields = [
            "id",
            "name",
            "description",
            "house",
            "house_id",
            "members",
            "allow_assign_member",
        ]
        extra_kwargs = {
            "description": {"required": False},
        }
        no_update_fields = ["house_id"]

    def get_is_allow_assign_member(self, obj):
        user = self.context.get("request").user
        return obj.is_allow_assign_member(user)

    def update(self, instance, validated_data):
        room = instance
        return room.update(
            name=validated_data.get("name", None),
            description=validated_data.get("description", None),
        )

    def create(self, validated_data):
        user = self.context.get("request").user
        house_id = validated_data.pop("house_id", None)
        try:
            house = models.House.objects.get(id=house_id)
            room = models.Room.create_new(
                name=validated_data.get("name", ""),
                description=validated_data.get("description", ""),
                house=house,
            )
            permission_models.Permission.grant_all_room_permissions(user, room)
            return room
        except models.House.DoesNotExist:
            raise serializers.ValidationError("House not found")


class CRUHouseDetail(
    serializers.ModelSerializer, mixin_serializers.NoUpdateSerializer
):
    class CRRoomBasic(serializers.ModelSerializer):
        """
        This Serializer is for used nested in HouseSerializer
        for create room with house at the same time.
        Otherwise, use `CRURoomDetail` instead.
        """

        accessible = serializers.SerializerMethodField(
            method_name="is_current_user_accessible"
        )

        def is_current_user_accessible(self, obj):
            user = self.context.get("request").user
            return obj.is_allow_access(user)

        class Meta:
            model = models.House
            fields = ["id", "name", "description", "address", "accessible"]

    # NOTE: Read house member use this field
    members = user_serializers.ReadBasicUserProfile(many=True, read_only=True)

    # NOTE: Set house members use this field
    member_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=True
    )
    # NOTE: set house owners use this field
    owner_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=True
    )
    rooms = CRRoomBasic(many=True, required=False)
    is_owner = serializers.SerializerMethodField(method_name="get_is_owner")

    class Meta:
        model = models.House
        fields = [
            "id",
            "name",
            "description",
            "address",
            "members",
            "member_ids",
            "owner_ids",
            "is_owner",
            "rooms",
        ]
        no_update_fields = ["member_ids", "owner_ids"]
        extra_kwargs = {
            "description": {"required": False},
            "address": {"required": False},
        }

    def get_is_owner(self, obj):
        house = obj
        request = self.context.get("request")
        if request.user.is_authenticated:
            user = request.user
            return permission_models.Permission.is_house_owner(user, house)
        return False

    def validate_member_ids(self, value):
        if not len(value):
            raise serializers.ValidationError(
                "At least one member is required"
            )
        return value

    def validate_owner_ids(self, value):
        if not len(value):
            raise serializers.ValidationError("At least one owner is required")
        return value

    def validate(self, attrs):
        if not self.instance:
            member_ids = attrs.get("member_ids", [])
            owner_ids = attrs.get("owner_ids", [])

            self.validate_owners_members_ids(
                member_ids=member_ids, owner_ids=owner_ids
            )
        return super().validate(attrs)

    def update(self, instance, validated_data):
        house = instance
        # If member_ids is not None, update the members

        return house.update(
            name=validated_data.get("name", None),
            description=validated_data.get("description", None),
            address=validated_data.get("address", None),
        )

    def create(self, validated_data):
        member_ids = validated_data.pop("member_ids", [])
        owner_ids = validated_data.pop("owner_ids", [])

        members = []
        if member_ids:
            members = User.objects.from_ids(*member_ids)

        if not len(members):
            raise serializers.ValidationError("User not found")

        owners = list(filter(lambda mem: mem.id in owner_ids, members))

        # Create house
        house = models.House.create_new(
            members=members,
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

        # Grant permission
        for user in owners:
            permission_models.Permission.grant_houses_owner_permissions(
                user, house
            )

            rooms = house.rooms.all()
            permission_models.Permission.grant_all_room_permissions(
                user, *rooms
            )

        return house

    def validate_owners_members_ids(self, member_ids, owner_ids):
        if not owner_ids:
            raise serializers.ValidationError("At least one owner is required")

        if bool(member_ids) ^ bool(owner_ids):
            raise serializers.ValidationError(
                "Include both member_ids and owner_ids for updating otherwise exclude both"
            )

        if len(owner_ids) > len(member_ids):
            raise serializers.ValidationError(
                "User must be a member instead to be an owner"
            )
        if not list_utils.is_subset_list(member_ids, owner_ids):
            raise serializers.ValidationError(
                "Owner must be a member of the house"
            )


# class URoomMember(serializers.ModelSerializer):
#     class RoomPermission(serializers.ModelSerializer):
#         class Meta:
#             model = permission_models.Permission
#             fields = ["permission_type", "user"]

#         def create(self, validated_data):
#             permission_models.Permission.grant_rooms_permission(
#                 user=validated_data.get("user"),
#             )

#     class Meta:
#         model = User
#         fields = ["id", "name", "description"]
