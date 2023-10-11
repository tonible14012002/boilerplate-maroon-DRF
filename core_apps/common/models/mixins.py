from django.db.models import ManyToManyField


class UpdateModelFieldMixin():
    def update(self, auto_save=True, **field):
        for field, val in field.items():
            attr = getattr(self, field)
            if isinstance(attr, ManyToManyField):
                attr.set(val)
            else:
                setattr(self, field, val)
        return self
