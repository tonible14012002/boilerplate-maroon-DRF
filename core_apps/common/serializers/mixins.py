

class SerialzierValidator():
    # Ensure validated data includes all fields and None is only used as a value when it's
    # the default value for a field.
    def validate(self, data):
        print("data:", data)
        print("fields: ", self.fields.items())
        # ...
        for field_name, field in self.fields.items():
            if field_name not in data:
                data[field_name] = field.initial
            elif data[field_name] is None and data[field_name] != field.initial:
                data[field_name] = field.initial
        return data
