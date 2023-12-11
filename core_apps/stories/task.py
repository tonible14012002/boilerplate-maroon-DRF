from django.contrib.auth import get_user_model
from . import story_inbox
import celery
from celery.signals import worker_process_init, worker_process_shutdown


User = get_user_model()


@worker_process_init.connect
def init_worker(**kwargs):
    global db_conn
    print('Initializing database connection for worker.')


@worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    global db_conn
    if db_conn:
        print('Closing database connectionn for worker.')
        db_conn.close()


@celery.shared_task()
def boardcast_story_inbox(sender_id, story_id, ttl):
    inbox = story_inbox.StoryInbox(sender_id)
    inbox.send_story(story_id=story_id, ttl=ttl)
