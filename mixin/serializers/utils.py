from rest_framework import serializers


class NoUpdateMixin(serializers.ModelSerializer):
    def get_extra_kwargs(self):
        '''
        specify `no_update_fields` in Meta class to
      mark all fields that only allow `create` or `read`
        '''
        kwargs = super().get_extra_kwargs()
        no_update_fields = getattr(self.Meta, "no_update_fields", None)

        if self.instance and no_update_fields:
            for field in no_update_fields:
                kwargs.setdefault(field, {})
                kwargs[field]["read_only"] = True

        return kwargs
