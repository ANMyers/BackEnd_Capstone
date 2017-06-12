import factory
from Recognition.models import Project, ProjectDataset
from django.contrib.auth.models import User
from random import randint

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

class ProjectFactory(factory.django.DjangoModelFactory):
    """
    This class creates fake data for the User table in the database.

    ----Fields----
    name: factory.Faker('first_name'): fake name of the project
    algorithm: (string) : 'KNN' representing kmeans algorithm
    user: factory.SubFactory('Recognition.factories.UserFactory'): builds the user for this specific project

    Author:
        Adam Myers
    """

    class Meta:
        model = Project
    name = factory.Faker('bs')
    algorithm = 'KNN'
    user = factory.Iterator(User.objects.all())

def list_of_random_integers(length):
    new_list = list()
    for each in range(0, length):
        rand_int = randint(50, 200)
        new_list.append(rand_int)
    return new_list

class ProjectDatasetFactory(factory.django.DjangoModelFactory):
    """
    This class creates fake data for the User table in the database.

    ----Fields----
    name: factory.Faker('first_name'): fake name of the project
    name: (string) : 'KNN' representing kmeans algorithm
    user: factory.SubFactory('Recognition.factories.UserFactory'): builds the user for this specific project

    Author:
        Adam Myers
    """

    class Meta:
        model = ProjectDataset
    dataset = list_of_random_integers(4)
    user = factory.Iterator(User.objects.all())
    project = factory.Iterator(Project.objects.all())
