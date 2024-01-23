from rest_framework import serializers


class House:
    id = '31012'
    name = 'oijoijq'


class HouseDetailSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        pass


# class HouseSerializer(serializers.Serializer):
#     id = serializers.IntegerField(required=False)
#     name = serializers.CharField(max_length=255)
#     address = serializers.CharField(max_length=255)
#     price = serializers.IntegerField()
#     description = serializers.CharField(max_length=255)
#     image = serializers.CharField(max_length=255)
#     created_at = serializers.DateTimeField(required=False)
#     updated_at = serializers.DateTimeField(required=False)
#     deleted_at = serializers.DateTimeField(required=False)
#     user_id = serializers.IntegerField(required=False)
#     user = serializers.SerializerMethodField()

#     def create(self, validated_data):
#         return super().create(validated_data)

#     def update(self, instance, validated_data):
#         return super().update(instance, validated_data)


# serializer = HouseSerializer(data={'id': '12312'})
# serializer.is_valid()

# serializer.save()
