from django.db.models import Manager, QuerySet
from . import enums as notification_enums


class NotificationQuerySet(QuerySet):
    def filter_by_room(self, room):
        return self.filter(
            room=room,
        )

    def all_room_event_notifications(self):
        return self.filter(
            room__isnull=False,
            event_code__in=notification_enums.ROOM_NOTIFICATION_EVENT_CODES,
        )


class NotificationManager(Manager):
    def get_queryset(self) -> NotificationQuerySet:
        return NotificationQuerySet(self.model, using=self._db)
