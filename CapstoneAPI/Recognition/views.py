from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
import json
from Recognition.models import *
from sklearn.neighbors import NearestNeighbors

from sklearn.cluster import KMeans
import numpy as np

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

    login(request, user=new_user)

    # Return the token to the client
    data = json.dumps({"token":token.key})
    return HttpResponse(data, content_type='application/json')

@csrf_exempt
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
    req_body = json.loads(request.body.decode())
    token = req_body['token']
    # print("\n\n\nUser?: {}\n\n".format(request.user))

    try:
        token = Token.objects.get(key=token)
        user = User.objects.get(pk=token.user_id)
    except Token.DoesNotExist:
        data = json.dumps({"continue": False, "error": "User has not logged in."})
        return HttpResponse(data, content_type='application/json')

    project = Project.objects.get(user=user, name=req_body['project'], algorithm=req_body['algorithm'])

    column_name = 'dataset'
    datasets = list(ProjectDataset.objects.filter(user=user, project=project).values(column_name))

    list_of_indexs = [each['index'] for each in req_body['ignored']]

    results = reformat_from_query(datasets, list_of_indexs, column_name)

    print("\n\none row: {}\nremoved: {}\n".format(results['results'][0], results['removed']))

    kmeans = KMeans(n_clusters=2, precompute_distances=True, random_state=1, max_iter=10000).fit(results['results'][:499])

    prediction = kmeans.predict(results['results'][500:550])
    # kmeans.labels_
    # kmeans.cluster_centers_

    print("\n\n\ncenters: {}\n\n".format(kmeans.cluster_centers_))
    print("\n\n\nprediction?: {}\n\n".format(prediction))

    # print("\n\n\n---->>>{}\n\n".format(req_body))
    data = json.dumps({"results":"We got the dataset."})
    return HttpResponse(data, content_type='application/json')


def reformat_from_query(dataset, indexs_to_remove, column_name):

    formated_list = list()
    indexs_removed = set()

    for counter, one_set in enumerate(dataset):
        new_list = one_set[column_name].split(',')
        start = len(new_list) - 1
        for i in range(start, -1, -1):
            if i in indexs_to_remove:
                indexs_removed.add(i)
                del new_list[i]
            else:
                try:
                    new_list[i] = float(new_list[i])
                except ValueError:
                    del new_list[i]
                    indexs_removed.add(i)

        formated_list.append(new_list)

    results = {
        "results": formated_list,
        "removed": indexs_removed
    }
    return results


@csrf_exempt
def format_dataset(request):
    """
    This function allows user to upload there dataset against there choosen algorithm and outputs one dataset for the user to choose which value to ignore.

    Arguments:
        request (POST): Sends data from user's dataset to be analysed 
        
    Returns:     
        return (json):  "sample_set": one index of the list of datasets to use as an example for which 
                                indexes to ignore.
                        "indexs": list of tuples, each tuple has the index of the value, and the 
                                given value for each non-number value.
    
    Author:
        Adam Myers

    """
    req_body = json.loads(request.body.decode())
    token = req_body['token']

    try:
        token = Token.objects.get(key=token)
        user = User.objects.get(pk=token.user_id)
    except Token.DoesNotExist:
        data = json.dumps({"continue": False, "error": "User has not logged in."})
        return HttpResponse(data, content_type='application/json')

    try:
        Project.objects.get(user=user, name=req_body['project'], algorithm=req_body['algorithm'])
        data = json.dumps({"continue": False, "error": "You already have a project by that name. Please choose a different name for your project."})
        return HttpResponse(data, content_type='application/json')
    except Project.DoesNotExist:
        new_project = Project(user=user, name=req_body['project'], algorithm=req_body['algorithm'])
        new_project.save()
        
    list_of_data = req_body['dataset'].split('\n')

    reformated_list = list()
    dicts_of_ignored_values = set()

    dataset_quantity = 0

    for counter, dataset in enumerate(list_of_data):
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
            dataset_quantity = dataset_quantity + 1
            new_string = ','.join(str(value) for value in new_list)
            dataset = ProjectDataset(user=user, project=new_project, dataset=new_string)
            dataset.save()
        if counter == 1:
            sample_set = new_list
            

# This will be used to determine which algorith will fit their dataset based off of amount of numbers per set.
# Once a tree structure algorithm is implemented site can allow a majority of words in their dataset but thats Recognition 2.0
    # percentage = percentage_of_numbers(sample_set)

    # if algorithm == 'Nearest Neighbor':
    #     if percentage > 0.75:
    #         go_on = True
    #     else:
    #         go_on = False
    # else:
    #     go_on = True
    go_on = True

    dicts_of_ignored_values = list(dicts_of_ignored_values)
    data = json.dumps({"sample_set":sample_set, "indexs": dicts_of_ignored_values, "continue": go_on, "amount": dataset_quantity})
    return HttpResponse(data, content_type='application/json')


def percentage_of_numbers(sample):
    numbers = 0
    total = 0
    for each in sample:
        try:
            float(each)
            numbers = numbers + 1
            total = total + 1
        except ValueError:
            total = total + 1

    return numbers / total

@csrf_exempt
def my_saved(request):

    req_body = json.loads(request.body.decode())

    try:
        token = Token.objects.get(key=req_body['token'])
        user = User.objects.get(pk=token.user_id)
    except Token.DoesNotExist:
        data = json.dumps({"continue": False, "error": "User has not logged in."})
        return HttpResponse(data, content_type='application/json')

    my_saved = list(Project.objects.filter(user=user).values('name'))

    data = json.dumps({"continue": True, "my_saved": my_saved})
    return HttpResponse(data, content_type='application/json')
