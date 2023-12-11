from django.contrib.auth import get_user_model
from . import story_inbox
import celery

User = get_user_model()


@celery.shared_task()
def boardcast_story_inbox(sender_id, story_id, ttl):
    inbox = story_inbox.StoryInbox(sender_id)
    inbox.send_story(story_id=story_id, ttl=ttl)
