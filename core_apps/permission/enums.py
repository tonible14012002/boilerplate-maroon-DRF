from django.db import models


class PermissionTypeChoices(models.TextChoices):
    # HOUSE PERMISSION
    REMOVE_HOUSE = (
        "REMOVE_HOUSE",
        "Remove house",
    )  # Allow to Update, Delete House
    INVITE_HOUSE_MEMBER = (
        "INVITE_HOUSE_MEMBER",
        "Invite house member",
    )  # Allow invite user to house
    REMOVE_HOUSE_MEMBER = (
        "REMOVE_HOUSE_MEMBER",
        "Remove house member",
    )  # Allow remove user from house

    # ROOM PERMISSION
    ACCESS_ROOM = ("ACCESS", "Access")  # Allow to access room
    ASSIGN_MEMBER = ("ASSIGN", "Assign")  # Allow to assign user to room
    DELETE_ROOM = ("DELETE", "Delete")  # Allow to delete room
    RECEIVE_ROOM_NOTIFICATION = (
        "RECEIVE_NOTIFICATION",
        "Receive Notification",
    )  # Receive room detection
    REMOVE_ROOM_MEMBER = (
        "REMOVE_MEMBER",
        "Remove Member",
    )  # Remove member from room
    ASSIGN_ROOM_PERMISSION = (
        "ASSIGN_ROOM_PERMISSION",
        "Assign Room Permission",
    )  # Assign room permission

    @classmethod
    def get_all_house_owner_permission_choices(cls):
        return [
            cls.REMOVE_HOUSE,
            cls.INVITE_HOUSE_MEMBER,
            cls.REMOVE_HOUSE_MEMBER,
        ]


HOUSE_PERMISSIONS = [
    PermissionTypeChoices.REMOVE_HOUSE,
    PermissionTypeChoices.INVITE_HOUSE_MEMBER,
    PermissionTypeChoices.REMOVE_HOUSE_MEMBER,
]

ROOM_PERMISSIONS = [
    PermissionTypeChoices.ACCESS_ROOM,
    PermissionTypeChoices.ASSIGN_MEMBER,
    PermissionTypeChoices.DELETE_ROOM,
    PermissionTypeChoices.RECEIVE_ROOM_NOTIFICATION,
    PermissionTypeChoices.REMOVE_ROOM_MEMBER,
    PermissionTypeChoices.ASSIGN_ROOM_PERMISSION,
]


def get_description(value):
    descriptions = {
        "INVITE_HOUSE_MEMBER": "Allow invite user to house",
        "REMOVE_HOUSE_MEMBER": "Allow remove user from house",
        "ACCESS_ROOM": "Allow to access room",
        "ASSIGN_MEMBER": "Allow to assign user to room",
        "DELETE_ROOM": "Allow to delete room",
        "RECEIVE_ROOM_NOTIFICATION": "Receive room detection",
        "REMOVE_ROOM_MEMBER": "Remove member from room",
        "ASSIGN_ROOM_PERMISSION": "Assign room permission",
    }
    return descriptions.get(value, "Description not available")
