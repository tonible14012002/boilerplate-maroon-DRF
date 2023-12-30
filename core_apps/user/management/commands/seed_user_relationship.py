from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model
from random import sample

User = get_user_model()


class Command(BaseCommand):
    help = 'Generate random follow relationships'

    def add_arguments(self, parser):
        parser.add_argument('follow_count', type=int, help='Number of random follow relationships to generate')

    def handle(self, *args, **options):
        follow_count = options['follow_count']

        with transaction.atomic():
            users = User.tests.only('pk')
            user_pks = [user.pk for user in users]

            # Generate random follow relationships
            for _ in range(follow_count):
                random_user_pairs = sample(user_pks, 2)
                user = User.tests.get(pk=random_user_pairs[0])
                to_follow = User.objects.get(pk=random_user_pairs[1])
                to_follow.followers.add(user)

        self.stdout.write(self.style.SUCCESS('Random follow relationships generated successfully.'))
