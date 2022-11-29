from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Populates the db with users that can login to the TAA portal'

    def handle(self, *args, **options):
        try:
            User.objects.create_user('pencil', password="password")
            User.objects.create_user('flower', password="password")
            User.objects.create_user('icecream', password="password")
            User.objects.create_user('basketball', password="password")
            User.objects.create_user('orange', password="password")
            User.objects.create_user('placeholder', password="password")

            self.stdout.write(self.style.SUCCESS('Successfully created db users'))
        except Exception as ex:
            raise CommandError(f'An error occurred: {ex}')
