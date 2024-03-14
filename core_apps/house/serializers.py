from rest_framework import serializers
from core_apps.user import serializers as user_serializers
from core_apps.device import serializers as device_serializers
from core_apps.permission import models as permission_models
from core_apps.permission import enums as permission_enums
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q
from mixin import serializers as mixin_serializers
from utils import list as list_utils
from . import models

User = get_user_model()


class RHouseBasic(serializers.ModelSerializer):
    class Meta:
        model = models.House
        fields = [
            "id",
            "name",
            "address",
            "description",
        ]


class CRURoomDetail(
    serializers.ModelSerializer, mixin_serializers.NoUpdateSerializer
):
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
    # Keep for backward compatibility
    allow_assign_member = serializers.SerializerMethodField(
        method_name="get_is_allow_assign_member"
    )

    room_permissions = serializers.SerializerMethodField(
        method_name="get_room_permissions"
    )

    devices = device_serializers.CRUDevice(many=True, read_only=True)

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
            "room_permissions",
            "devices",
        ]
        extra_kwargs = {
            "description": {"required": False},
        }
        no_update_fields = ["house_id"]

    def get_is_allow_assign_member(self, obj):
        user = self.context.get("request").user
        return obj.is_allow_assign_member(user)

    def get_room_permissions(self, obj):
        room = obj
        room_permissions = (
            permission_models.Permission.get_user_room_permissions(
                user=self.context.get("request").user, room=room, flat=True
            )
        )
        return room_permissions

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

        # Keep for backward compatibility
        accessible = serializers.SerializerMethodField(
            method_name="is_current_user_accessible"
        )

        room_permissions = serializers.SerializerMethodField(
            method_name="get_room_permissions"
        )

        def get_room_permissions(self, obj):
            user = self.context.get("request").user
            room = obj
            return permission_models.Permission.get_user_room_permissions(
                user=user, room=room, flat=True
            )

        def is_current_user_accessible(self, obj):
            user = self.context.get("request").user
            return obj.is_allow_access(user)

        class Meta:
            model = models.House
            fields = [
                "id",
                "name",
                "description",
                "address",
                "accessible",
                "room_permissions",
            ]

    class RDevice(device_serializers.CRUDevice):
        allow_access = serializers.SerializerMethodField(
            method_name="is_allow_access"
        )

        class Meta(device_serializers.CRUDevice.Meta):
            fields = device_serializers.CRUDevice.Meta.fields + [
                "allow_access"
            ]

        def is_allow_access(self, obj):
            room = obj.room
            user = self.context.get("request").user
            return room.is_allow_access(user)

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
    house_permissions = serializers.SerializerMethodField(
        method_name="get_house_permissions"
    )

    devices = RDevice(
        many=True, source="get_all_devices_in_rooms", read_only=True
    )

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
            "devices",
            "house_permissions",
        ]
        no_update_fields = ["member_ids", "owner_ids"]
        extra_kwargs = {
            "description": {"required": False},
            "address": {"required": False},
        }

    def get_house_permissions(self, obj):
        user = self.context.get("request").user
        house = obj
        return permission_models.Permission.get_user_house_permissions(
            user=user, house=house, flat=True
        )

    def get_is_owner(self, obj):
        house = obj
        request = self.context.get("request")
        if request.user.is_authenticated:
            user = request.user
            return house.is_user_owner(user)
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

            self._validate_owners_members_ids(
                member_ids=member_ids, owner_ids=owner_ids
            )
        return super().validate(attrs)

    def update(self, instance, validated_data):
        from core_apps.notification.models import Notification

        house = instance
        to_update_fields = [
            field for field in validated_data if field in validated_data
        ]

        old_values = [getattr(house, f) for f in to_update_fields]

        Notification.create_update_house_metadata_notification(
            house=house,
            updator=self.context.get("request").user,
            update_field_names=to_update_fields,
            old_values=old_values,
        )

        house.update(
            name=validated_data.get("name", None),
            description=validated_data.get("description", None),
            address=validated_data.get("address", None),
        )
        return house

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

    def _validate_owners_members_ids(self, member_ids, owner_ids):
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


class AddHouseMember(serializers.Serializer):
    class HouseMemberWithPermissionSerializer(serializers.Serializer):
        id = serializers.UUIDField(required=True, write_only=True)
        house_permissions = serializers.ListField(
            child=serializers.CharField(), required=True
        )

        def validate_house_permissions(self, value):
            if not list_utils.is_subset_list(
                permission_enums.HOUSE_PERMISSIONS, value
            ):
                raise serializers.ValidationError(
                    "Incorrect permission enum value"
                )
            return value

    add_members = HouseMemberWithPermissionSerializer(
        many=True, required=True, write_only=True
    )
    house_id = serializers.UUIDField(required=True, write_only=True)

    def validate_members(self, value):
        if not len(value):
            raise serializers.ValidationError(
                "At least one member is required"
            )
        return value

    def create(self, validated_data):
        from core_apps.permission.models import Permission, PermissionType
        from core_apps.notification.models import Notification

        to_add_members = validated_data["add_members"]
        house_id = validated_data["house_id"]

        permission_types = PermissionType.objects.filter(
            name__in=set(
                permission
                for member_data in to_add_members
                for permission in member_data["house_permissions"]
            )
        )

        permission_type_mapping = {
            permission_type.name: permission_type
            for permission_type in permission_types
        }

        members = User.objects.filter(
            id__in=set([member["id"] for member in to_add_members])
        )

        members_mapping = {member.id: member for member in members}

        permission_to_create = [
            Permission(
                permission_type=permission_type_mapping[permission],
                user=members_mapping[member_data["id"]],
            )
            for member_data in to_add_members
            for permission in member_data["house_permissions"]
        ]

        Permission.objects.bulk_create(
            permission_to_create,
            ignore_conflicts=True,
        )

        query = Q()
        for member_data in to_add_members:
            query |= Q(
                user__id=member_data["id"],
                permission_type__name__in=member_data["house_permissions"],
            )

        house = models.House.objects.get(id=house_id)
        correspond_permissions = Permission.objects.filter(query)
        for p in correspond_permissions:
            p.houses.add(house)

        users = User.objects.filter(
            id__in=[member["id"] for member in to_add_members]
        )
        house.members.add(*users)

        # Notification
        Notification.create_add_house_member_notification(
            house=house,
            invitor=self.context.get("request").user,
            new_members=users,
        )
        # FIXME: Fire notifications to all house members except invitor.
        return house


class RemoveHouseMember(serializers.Serializer):
    remove_members = serializers.ListField(
        child=serializers.UUIDField(), required=True, write_only=True
    )

    def validate_remove_members(self, value):
        if not len(set(value)) == len(value):
            raise serializers.ValidationError("Duplicate member id")
        return value


class RoomMember(user_serializers.ReadBasicUserProfile):
    """
    Include room_id in context for getting room_permissions
    """

    room_permissions = serializers.SerializerMethodField(
        method_name="get_room_permissions"
    )

    def get_room_permissions(self, obj):
        room_id = self.context.get("room_id")
        room = get_object_or_404(models.Room, id=room_id)
        user = obj
        return permission_models.Permission.get_user_room_permissions(
            user=user, room=room, flat=True
        )

    class Meta:
        model = User
        fields = user_serializers.ReadBasicUserProfile.Meta.fields + [
            "room_permissions",
        ]


class HouseMember(user_serializers.ReadBasicUserProfile):
    house_permissions = serializers.SerializerMethodField(
        method_name="get_house_permissions"
    )

    class Meta:
        model = User
        fields = user_serializers.ReadBasicUserProfile.Meta.fields + [
            "house_permissions",
        ]

    def get_house_permissions(self, obj):
        house_id = self.context.get("house_id")
        house = get_object_or_404(models.House, id=house_id)
        user = obj
        return permission_models.Permission.get_user_house_permissions(
            house=house, user=user, flat=True
        )


class UHouseMember(serializers.ModelSerializer):
    """
    Include `house_id` in serializer context for getting house_permissions
    """

    update_house_permissions = serializers.MultipleChoiceField(
        write_only=True, choices=permission_enums.HOUSE_PERMISSIONS
    )
    house_permissions = serializers.SerializerMethodField(
        method_name="get_house_permissions"
    )

    class Meta:
        model = User
        fields = ["id", "house_permissions", "update_house_permissions"]

    def get_house_permissions(self, obj):
        house_id = self.context.get("house_id")
        user = obj
        house = get_object_or_404(models.House, id=house_id)
        return permission_models.Permission.get_user_house_permissions(
            user=user, house=house, flat=True
        )

    def update(self, instance, validated_data):
        user = instance
        house_id = self.context.get("house_id")
        user_house_permission_names = validated_data.get(
            "update_house_permissions", []
        )
        permission_models.Permission.remove_house_permissions(
            user_id=user.id,
            house_id=house_id,
            permission_names=permission_enums.HOUSE_PERMISSIONS,
        )
        permission_models.Permission.grant_houses_permissions(
            user,
            user_house_permission_names,
            get_object_or_404(models.House, id=house_id),
        )
        return user


class URoomMember(serializers.ModelSerializer):
    """
    REQUIRED: Include `room` instance in serializer context
    """

    update_room_permissions = serializers.MultipleChoiceField(
        write_only=True, choices=permission_enums.ROOM_PERMISSIONS
    )
    room_permissions = serializers.SerializerMethodField(
        method_name="get_room_permissions"
    )

    class Meta:
        model = User
        fields = ["id", "room_permissions", "update_room_permissions"]

    def get_room_permissions(self, obj):
        room = self.context.get("room")
        user = obj
        return permission_models.Permission.get_user_room_permissions(
            user=user, room=room, flat=True
        )

    def update(self, instance, validated_data):
        user = instance
        room = self.context.get("room")
        user_room_permission_names = validated_data.get(
            "update_room_permissions", []
        )
        permission_models.Permission.remove_user_room_permissions(
            user_id=user.id,
            room_id=room.id,
            permission_names=permission_enums.ROOM_PERMISSIONS,
        )
        permission_models.Permission.grant_rooms_permissions(
            user, user_room_permission_names, room
        )
        return user


class AddRoomMember(serializers.Serializer):
    class RoomMemberWithPermissionSerializer(serializers.Serializer):
        id = serializers.UUIDField(required=True, write_only=True)
        room_permissions = serializers.ListField(
            child=serializers.CharField(), required=True
        )

        def validate_room_permissions(self, value):
            if not list_utils.is_subset_list(
                permission_enums.ROOM_PERMISSIONS, value
            ):
                raise serializers.ValidationError(
                    "Incorrect room permission enum value"
                )
            return value

    add_members = RoomMemberWithPermissionSerializer(
        many=True, required=True, write_only=True
    )
    room_id = serializers.UUIDField(required=True, write_only=True)

    def validate_add_members(self, value):
        if not len(value):
            raise serializers.ValidationError(
                "At least one member is required"
            )
        return value

    def create(self, validated_data):
        from core_apps.notification.models import Notification

        to_add_members = validated_data["add_members"]
        room_id = validated_data["room_id"]

        room = models.Room.objects.select_related("house").get(id=room_id)
        new_members = User.objects.filter(
            id__in=set([member["id"] for member in to_add_members])
        )

        members_mapping = {member.id: member for member in new_members}

        is_valid = self._is_house_member(
            list(members_mapping.keys()), room.house
        )

        if not is_valid:
            raise serializers.ValidationError("User not member of houses")

        self._create_permisison_users(to_add_members, members_mapping, room)

        Notification.create_add_room_member_notification(
            room=room,
            invitor=self.context.get("request").user,
            new_members=new_members,
        )

        return room

    def _is_house_member(self, user_ids, house):
        """
        Check users are members of the house and have'nt added to room"""
        total_house_members = house.members.filter(id__in=user_ids).count()
        # check if any user already has permission to access room

        return total_house_members == len(user_ids)

    def _get_permission_mapping(self, add_members_data):
        from core_apps.permission.models import PermissionType

        permission_types = PermissionType.objects.filter(
            name__in=[
                *set(
                    permission
                    for member_data in add_members_data
                    for permission in member_data["room_permissions"]
                ),
                permission_enums.PermissionTypeChoices.ACCESS_ROOM,
            ]
        )

        permission_type_mapping = {
            permission_type.name: permission_type
            for permission_type in permission_types
        }
        return permission_type_mapping

    def _create_permisison_users(
        self, add_members_data, members_mapping, room
    ):
        from core_apps.permission.models import Permission
        from core_apps.permission.enums import PermissionTypeChoices

        permission_type_mapping = self._get_permission_mapping(
            add_members_data
        )

        permission_to_create = [
            Permission(
                permission_type=permission_type_mapping[permission_name],
                user=members_mapping[member_data["id"]],
            )
            for member_data in add_members_data
            for permission_name in member_data["room_permissions"]
        ]

        # Access room as default permission
        for member_data in add_members_data:
            permission_to_create.append(
                Permission(
                    permission_type=permission_type_mapping[
                        PermissionTypeChoices.ACCESS_ROOM
                    ],
                    user=members_mapping[member_data["id"]],
                )
            )

        Permission.objects.bulk_create(
            permission_to_create, ignore_conflicts=True
        )

        query = Q()
        for member_data in add_members_data:
            query |= Q(
                user_id=member_data["id"],
                permission_type__name__in=member_data["room_permissions"],
            )
        correspond_permissions = Permission.objects.filter(query)

        for p in correspond_permissions:
            p.rooms.add(room)

        return correspond_permissions
