from django.contrib.auth import models


class UserManager(models.UserManager):
    def from_ids(self, *ids):
        return self.filter(id__in=ids)
