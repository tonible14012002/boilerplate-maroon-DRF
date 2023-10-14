from typing import Any
from django.core import management
from django.core.management.base import CommandParser
from django.contrib import auth
from ... import enums
from ... import models
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

        for _ in range(total_stories):
            user = random.choice(random_users)
            duration_choices = [10, 15, 30]
            models.UserStory.create_new(
                user=user,
                privacy_mode=enums.PrivacyMode.Public[1],
                media_type=enums.MediaType.Image[1],
                media_url="",
                live_time=86400,
                duration=random.choice(duration_choices)
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {total_stories} stories for random users.'))
