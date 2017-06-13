from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
import json
from Recognition.models import *

# Create your views here.
@csrf_exempt
def register_user(request):
    '''Handles the creation of a new user for authentication
    Method arguments:
      request -- The full HTTP request object
    '''

    # Load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
                    username=req_body['username'],
                    password=req_body['password'],
                    email=req_body['email'],
                    first_name=req_body['first_name'],
                    last_name=req_body['last_name'],
                    )

    # Commit the user to the database by saving it
    new_user.save()

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)

    # Return the token to the client
    data = json.dumps({"token":token.key})
    return HttpResponse(data, content_type='application/json')

def kmeans(request):
    """
    This function allows user to run kmeans alogrithm on their dataset.

    Arguments:
        request (POST): Sends data from user's dataset to be analysed 
        
    Returns:     
        return (dictionary): data from the results of running the algorithm
    
    Author:
        Adam Myers

    """
    pass

@csrf_exempt
def format_dataset(request):
    """
    This function allows user to upload there dataset against there choosen algorithm and outputs one dataset for the user to choose which value to ignore.

    Arguments:
        request (POST): Sends data from user's dataset to be analysed 
        
    Returns:     
        return (dictionary): data from the results of running the algorithm
    
    Author:
        Adam Myers

    """
    req_body = json.loads(request.body.decode())
    list_of_data = req_body['dataset'].split('\n')
    algorithm = req_body['algorithm']

    reformated_list = list()
    dicts_of_ignored_values = set()

    for dataset in list_of_data:
        new_list = dataset.split(',')
        append = True
        for index, value in enumerate(new_list):
            try:
                new_list[index] = float(value)
            except ValueError:
                if len(value) == 0:
                    append = False
                else:
                    new_tuple = (index, value)
                    dicts_of_ignored_values.add(new_tuple)

        if append:
            reformated_list.append(new_list)

    sample_set = reformated_list[0]
    dicts_of_ignored_values = list(dicts_of_ignored_values)
    data = json.dumps({"sample_set":sample_set, "indexs": dicts_of_ignored_values})
    return HttpResponse(data, content_type='application/json')


