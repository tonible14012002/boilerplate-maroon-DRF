from typing import Any
from django.core import management
from django.core.management.base import CommandParser
from django.contrib import auth
from ... import enums
from ... import models
from ...import story_inbox
import json
import random

User = auth.get_user_model()


class Command(management.BaseCommand):
    help = "Generate random stories for random users with a 1 day expire"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('total_stories', type=int, help="Number of stories to be generated")

    def handle(self, *args: Any, **options: Any) -> str | None:
        total_stories = options['total_stories']

        random_users = User.tests.order_by('?')
        if not random_users.count():
            self.stdout.write(self.style.ERROR('No test users founded, please seed users first'))
            return

        story_schema = {
            'user': '...random-user...',
            'privacy_mode': 'Public',
            'media_type': 'IMAGE',
            'media_url': '',
            'live_time': 86400,
            'duration': 'randome in set (10, 15, 30)',
            'alt_text': 'gened Alt text',
            'caption': 'Story caption fot testing',
        }

        self.stdout.write(self.style.WARNING(
            f'''Seed stories will be own by random users created using \'seed_users\' cmd.\n
                 The schema for stories is following:
                {json.dumps(story_schema, indent=2)}''',
        ))
        self.stdout.write(self.style.WARNING('Seeding stories...'))

        for _ in range(total_stories):
            user = random.choice(random_users)
            duration_choices = [10, 15, 30]
            story = models.UserStory.create_new(
                user=user,
                privacy_mode=enums.PrivacyMode.Public,
                media_type=enums.MediaType.Image[1],
                media_url="",
                live_time=86400,
                duration=random.choice(duration_choices),
                alt_text=story_schema['alt_text'],
                caption=story_schema['caption']
            )
            inbox = story_inbox.StoryInbox(user.id)
            inbox.broadcast_story(story_id=story.id, ttl=story.live_time)

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {total_stories} stories for random users.'))
