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
            users = User.objects.only('pk')
            user_pks = [user.pk for user in users]

            # Generate random follow relationships
            random_user_pairs = sample(user_pks, 2 * follow_count)
            for i in range(0, len(random_user_pairs), 2):
                from_user_pk = random_user_pairs[i]
                to_user_pk = random_user_pairs[i + 1]

                from_user = User.objects.get(pk=from_user_pk)
                to_user = User.objects.get(pk=to_user_pk)
                from_user.followers.add(to_user)

        self.stdout.write(self.style.SUCCESS('Random follow relationships generated successfully.'))