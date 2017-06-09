import factory
from Recognition.models import *
from django.contrib.auth.models import User

class UserFactory(factory.django.DjangoModelFactory):
    """
    This class creates fake data for the User table in the database.

    ----Fields----
    username: factory.Faker('word'): fake username of a user
    first_name: factory.Faker('first_name'): fake first name of a user
    last_name: factory.Faker('last_name'): fake last name of a user
    email: factory.Faker('email'): fake email of a user
    password: factory.Faker('password'): password name of a user
    date_joined: factory.Faker('date'): fake date joined of a user
    last_login: factory.Faker('date'): fake date last logined in of a user
    is_superuser: 0: indicated user is not superuser
    is_staff: 0: indicated user is not staff
    is_active: 1: indicated user is active

    Author:
        Adam Myers
    """

    class Meta:
        model = User
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    username = factory.Faker('word')
    password = factory.Faker('password')
    date_joined = factory.Faker('date')
    last_login = factory.Faker('date')
    is_superuser = 0
    is_staff = 0
    is_active = 1