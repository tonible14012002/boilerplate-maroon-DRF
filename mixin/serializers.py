from rest_framework import serializers
from rest_framework.mixins import CreateModelMixin


class NoUpdateMixin:
    """
    specify no_update_fields in Meta class to make fields noy updateable
    """

    def mark_fields_not_updatable(self, kwargs):
        no_update_fields = getattr(self.Meta, "no_update_fields", [])
        if self.instance and no_update_fields:
            for field in no_update_fields:
                kwargs.setdefault(field, {})
                kwargs[field] = {"read_only": True}
        return kwargs


class NoUpdateSerializer(NoUpdateMixin, serializers.Serializer):
    def get_extra_kwargs(self, field_name, field_kwargs):
        kwargs = super().get_field_kwargs(field_name, field_kwargs)
        return self.mark_readonly(kwargs)
