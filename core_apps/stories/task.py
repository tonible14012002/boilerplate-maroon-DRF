from django.contrib.auth import get_user_model
from . import story_inbox
import celery

User = get_user_model()


@celery.shared_task()
def boardcast_story_inbox(sender_id, story_id, ttl):
    inbox = story_inbox.StoryInbox(sender_id)
    inbox.broadcast_story(story_id=story_id, ttl=ttl)


@celery.shared_task()
def send_active_stories_to(sender_id, user_id):
    inbox = story_inbox.StoryInbox(sender_id)
    inbox.send_all_active_story_to_user(user_id=user_id)
