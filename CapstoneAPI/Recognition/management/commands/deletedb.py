import os
from django.core import management
from django.core.management.base import BaseCommand
from django.core.management.commands import makemigrations

class Command(BaseCommand):
    """
    Defines the command 'deletedb', which is a shortcut for running
    the necessary shell commands to generate our database's tables and
    load our data to them via Faker. These commands are, in order:

    Commands Ran:
        rm Recognition/migrations/*.py
        touch Recognition/migrations/__init__.py
        rm db.sqlite3

    Author:
        Adam Myers
    """

    def handle(self, *args, **options):
        os.system('rm Recognition/migrations/*.py;')   #deletes all of the .py files in the migrations directory except for the __init__.py file.
        os.system('touch Recognition/migrations/__init__.py;') #re-create the __init__.py file.
        os.system('rm db.sqlite3;')  #deletes the database file.