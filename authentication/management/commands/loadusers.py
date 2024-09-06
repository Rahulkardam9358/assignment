from django.core.management.base import BaseCommand
from authentication.models import User
import json


class Command(BaseCommand):
    help = "Create users as per json data"

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Path to the file to process',
        )

    def handle(self, *args, **options):
        file_path = options.get('file')
        with open(file_path, 'r') as file:
            users = json.load(file)
            for user in users:
                User.objects.create_user(
                    user['email'], 
                    user['default_password'], 
                    first_name=user['first_name'], 
                    last_name=user['last_name']
                )
        self.stdout.write(self.style.SUCCESS(f'Added {len(users)} users'))