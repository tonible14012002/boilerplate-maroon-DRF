from django.db import models


class EventCodeChoices(models.TextChoices):
    # Devices Events
    DEVICE_FALL_DETECTED = "FALL_DETECTED", "Fall Detected"
    # House Events
    ADD_MEMBER_TO_HOUSE = "ADD_MEMBER_TO_HOUSE", "New Invite to House"
    REMOVE_MEMBER_FROM_HOUSE = "REMOVE_MEMBER_FROM_HOUSE", "Removed from House"
    UPDATE_HOUSE_METADATA = "UPDATE_HOUSE_METADATA", "House Metadata Updated"
    # Room Events
    INVITE_MEMBER_TO_ROOM = "INVITE_MEMBER_TO_ROOM", "Invited to Room"


DEVICE_NOTIFICATION_EVENT_CODES = [
    EventCodeChoices.DEVICE_FALL_DETECTED,
]

ROOM_NOTIFICATION_EVENT_CODES = [EventCodeChoices.INVITE_MEMBER_TO_ROOM]

HOUSE_NOTIFICATION_EVENT_CODES = [
    EventCodeChoices.ADD_MEMBER_TO_HOUSE,
    EventCodeChoices.REMOVE_MEMBER_FROM_HOUSE,
    EventCodeChoices.UPDATE_HOUSE_METADATA,
]
