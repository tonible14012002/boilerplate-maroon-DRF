from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import UserStory, StoryView
from core_apps.accounts import serializers as account_serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RStoryView(ModelSerializer):
    user = account_serializers.ReadBasicUserProfile()

    class Meta:
        model = StoryView
        fields = ['id', 'user', 'story', 'viewed_at']


class CRUStoryDetail(ModelSerializer):
    """
    Story serializer for archieved story
    Must pass in request context for `.create()`
    """

    views = RStoryView(many=True, source="story_views", read_only=True)
    excluded_users = account_serializers.ReadBasicUserProfile(many=True, read_only=True)
    users_to_exclude = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=True
    )
    owner = account_serializers.ReadBasicUserProfile(source="user", read_only=True)

    class Meta:
        model = UserStory
        fields = [
            'id', 'duration', 'excluded_users', 'media_url', 'created_at', 'updated_at',
            'live_time', 'status', 'privacy_mode', 'views', 'users_to_exclude', 'expire_date', 'media_type', 'owner'
        ]
        read_only_fields = ['status', 'views', 'expire_date']
        create_only_fields = ['duration', 'media_url', 'live_time']
        extra_kwargs = {
            'duration': {'required': True},
            'live_time': {'required': True},
            'privacy_mode': {'required': True},
            'media_type': {'required': True}
        }

    def get_fields(self):
        fields = super().get_fields()
        # media_url is not allowed in update
        if self.instance:
            # update
            fields['media_url'].required = False
        return fields

    def to_internal_value(self, data):
        valid_data = super().to_internal_value(data)
        if self.instance:
            # not allow in update
            for field in self.Meta.create_only_fields:
                valid_data.pop(field, None)
        return valid_data

    def create(self, validated_data):
        user_ids_to_exclude = validated_data.pop('users_to_exclude', [])
        user = self.context['request'].user
        story = UserStory.create_new(
            user=user,
            **validated_data
        )

        users_to_exclude = User.objects.from_ids(*user_ids_to_exclude)
        story.reset_exclude_users(users_to_exclude)
        return story

    def update(self, instance, validated_data):
        story = instance
        user_ids_to_exclude = validated_data.pop('users_to_exclude', [])
        users = User.objects.from_ids(*user_ids_to_exclude)
        story.reset_exclude_users(users)

        return story


class RFollowingStory(ModelSerializer):
    """
    Story serializer for friend viewpoint
    """
    owner = account_serializers.ReadBasicUserProfile(source="user", read_only=True)

    class Meta:
        model = UserStory
        fields = [
            'id', 'duration', 'media_url', 'created_at',
            'status', 'privacy_mode', 'expire_date', 'owner'
        ]
