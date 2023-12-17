from django.apps import apps


def get_user_story_model():
    return apps.get_model('stories', 'UserStory')


def get_story_view_model():
    return apps.get_model('stories', 'StoryView')
