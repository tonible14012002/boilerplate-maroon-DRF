from django.core import management
from core_apps.accounts import models
from django_countries.data import COUNTRIES
from core_apps.accounts import enums
import uuid
import random


class Command(management.BaseCommand):
    help = '''
        Generate random users with profiles
        The default password is 123456
        email = {username}@example.com
    '''
    countries = list(COUNTRIES.keys())
    city_names = [
        'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
        'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose',
        'Austin', 'Jacksonville', 'Indianapolis', 'San Francisco', 'Columbus',
        'Fort Worth', 'Charlotte', 'Seattle', 'Denver', 'El Paso'
    ]

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of users to generate')

    def handle(self, *args, **options):
        count = options['count']

        for _ in range(count):
            username = f'user_{uuid.uuid1()}'
            email = f'{username}@example.com'
            password = '123456'  # You can set the password as needed

            models.MyUser.create_register(
                username=username,
                password=password,
                extra_fields={
                    'email': email,
                },
                profile_fields={
                    'country': random.choice(self.countries),
                    'city': random.choice(self.city_names),
                    'avatar': '',
                    'gender': random.choice(enums.Gender.choices)[1]
                },
                is_test=True
            )
            self.stdout.write(self.style.SUCCESS(f'User {username} created'))