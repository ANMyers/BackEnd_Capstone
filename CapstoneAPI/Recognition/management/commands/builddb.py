from django.core import management
from django.core.management.base import BaseCommand
from django.core.management.commands import makemigrations
from Recognition.factories import *

class Command(BaseCommand):
    """
    Defines the command 'builddb', which is a shortcut for running
    the necessary shell commands to generate our database's tables and
    load our data to them via Faker. 

    Commands Ran:
        python manage.py makemigrations api
        python manage.py migrate
        (Factory Calls): UserFactory.create_batch(size=10)

    Author: Adam Myers
    """

    def handle(self, *args, **options):
        management.call_command('makemigrations')
        management.call_command('migrate')
        UserFactory.create_batch(size=10)