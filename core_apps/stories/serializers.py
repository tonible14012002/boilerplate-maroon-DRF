from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import UserStory, StoryView
from core_apps.profiles.serializers import SimpleProfileSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class StoryViewSerializer(ModelSerializer):
    user = SimpleProfileSerializer()

    class Meta:
        model = StoryView
        fields = ['id', 'user', 'story', 'viewed_at']


class UserStoryDetailSerializer(ModelSerializer):
    """
    Story serializer for archieved story
    Must pass in request context for `.create()`
    """

    views = StoryViewSerializer(many=True, source="story_views", read_only=True)
    excluded_users = SimpleProfileSerializer(many=True, read_only=True)
    users_to_exclude = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = UserStory
        fields = [
            'id', 'duration', 'excluded_users', 'media_url', 'created_at', 'updated_at',
            'live_time', 'status', 'privacy_mode', 'views', 'users_to_exclude', 'expire_date'
        ]
        read_only_fields = ['status', 'views', 'expire_time']
        extra_kwargs = {
            'excluded_users': {'required': False}
        }
        create_only_fields = ['duration', 'media_url', 'live_time']

    def get_fields(self):
        fields = super().get_fields()
        if self.instance:
            # update
            fields['media_url'].required = False
        return fields

    def to_internal_value(self, data):
        valid_data = super().to_internal_value(data)
        if self.instance:
            # update
            for field in self.Meta.create_only_fields:
                valid_data.pop(field, None)
        return data

    def create(self, validated_data):
        user_ids_to_exclude = validated_data.pop('users_to_exclude', [])
        user = self.context['request'].user
        story = UserStory.objects.create(
            user=user,
            **validated_data
        )

        users_to_exclude = User.objects.filter(id__in=user_ids_to_exclude)
        story.excluded_users.set(users_to_exclude)
        story.save()
        return story

    def update(self, instance, validated_data):
        story = instance
        user_ids_to_exclude = validated_data.pop('users_to_exclude', [])
        users = User.objects.filter(id__in=user_ids_to_exclude)
        story.excluded_users.set(users)
        story.save()

        return story


class FriendStorySerializer(ModelSerializer):
    """
    Story serializer for friend viewpoint
    """
    owner = SimpleProfileSerializer(source="user", read_only=True)

    class Meta:
        model = UserStory
        fields = [
            'id', 'duration', 'media_url', 'created_at',
            'status', 'privacy_mode', 'expire_date'
        ]
