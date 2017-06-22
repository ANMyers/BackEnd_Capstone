from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse
import json

from Recognition.models import *

from sklearn.cluster import KMeans
from sklearn.svm import SVC as Support_Vector_Classification
from sklearn import preprocessing

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
def SVC(request):
    """
    This function allows user to run SVC alogrithm on their dataset.

    Arguments:
        request (POST): Sends data from user's dataset to be analysed 
        
    Returns:     
        return (dictionary): data from the results of running the algorithm
    
    Author:
        Adam Myers

    """
    # decode the request body and show me whats in it
    req_body = json.loads(request.body.decode())
    print("\n\n-------below was sent in request-------\n{}\n".format(req_body))

    # see if the is logged in (the hard way will refactor later)
    token = req_body['token']
    try:
        token = Token.objects.get(key=token)
        user = User.objects.get(pk=token.user_id)
    except Token.DoesNotExist:
        data = json.dumps({"continue": False, "error": "User has not logged in."})
        return HttpResponse(data, content_type='application/json')

    # grab user's project
    project = Project.objects.get(user=user, name=req_body['project'], algorithm=req_body['algorithm'])

    # grab dataset from user's project
    column_name = 'dataset'
    datasets = list(ProjectDataset.objects.filter(user=user, project=project).values(column_name))
    list_of_indexs = [each['index'] for each in req_body['ignored']]

    results = reformat_from_query(dataset=datasets, indexs_to_remove=list_of_indexs, column_name=column_name, algorithm=project.algorithm, predict_index=req_body['predict_index'])

    start = int(req_body['train_on'])
    stop = int(req_body['train_against'])

    train_on = results['results'][:start]
    train_on_y = results['y_list'][:start]

    train_against = results['results'][-stop:]

    preproc_train_on = preprocess_svc_data(train_on)
    preproc_train_y = preprocess_svc_data(train_on_y)
    preproc_train_against = preprocess_svc_data(train_against)

    supveccla = Support_Vector_Classification()

    try:
        supveccla.fit(preproc_train_on['processed'], preproc_train_y['processed'])
    except ValueError:
        labels = np.unique(preproc_train_y['processed'])
        print("\nlabels?: {}\n".format(labels))
        data = json.dumps({"error": True, "error_message": "The dataset you sent only has 1 predicted outcome. Please send more data to get a better result."})
        return HttpResponse(data, content_type='application/json')

    cluster_amount = len(supveccla.n_support_)
    pred = supveccla.predict(preproc_train_against['processed'])
    sep_clusters = seperate_clusters(supveccla.support_, cluster_amount)
    percent = calculate_percent(sep_clusters)

    print("\namount: {}\n".format(percent))

    # data = json.dumps({"results":prediction, "accuracy": relabeled_accuracy, "centroids": user_labels, "project": req_body['project'], "cluster_amount": cluster_quantity})
    data = json.dumps({"results": list(pred), "project": req_body['project'], "accuracy": percent,"cluster_amount": int(cluster_amount),  "project": req_body['project'], "algorithm": req_body['algorithm']})
    return HttpResponse(data, content_type='application/json')

def calculate_percent(cluster_dict):
    keys = cluster_dict.keys()
    total = 0

    for key in keys:
        total = total + len(cluster_dict[key])
    for key in keys:
        divided = len(cluster_dict[key]) / total
        cluster_dict[key] = round(divided * 100, 2)

    return cluster_dict


def seperate_clusters(cluster_index, number_of_clusters):
    counter = 0
    cluster_dict = dict()
    for i in range(0, len(cluster_index)):
        if i < len(cluster_index)-1:
            if cluster_index[i] < cluster_index[i+1]:
                try:
                    cluster_dict[counter].append(cluster_index[i])
                except KeyError:
                    cluster_dict[counter] = list()
                    cluster_dict[counter].append(cluster_index[i])
            else:
                cluster_dict[counter].append(cluster_index[i])
                counter += 1

    return cluster_dict


def preprocess_svc_data(train_data):
    train_data = np.array(train_data)
    index_labels = dict()
    indexes_to_preprocess = set()

    for p in range(0, len(train_data)):
        one_row = train_data[p]
        for i in range(0, len(one_row)):
            try:
                float(one_row[i])
            except ValueError:
                indexes_to_preprocess.add(i)

    for index in indexes_to_preprocess:
        le = preprocessing.LabelEncoder()
        le.fit(train_data[:,index])
        index_labels[index] = list(le.classes_)
        train_data[:,index] = le.transform(train_data[:,index])

    results = {
        "index_labels": index_labels,
        "processed": train_data
    }
    return results



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
    # decode the request body and show me whats in it
    req_body = json.loads(request.body.decode())
    print("\n\n-------below was sent in request-------\n{}\n".format(req_body))

    # see if the is logged in (the hard way will refactor later for django way)
    token = req_body['token']
    try:
        token = Token.objects.get(key=token)
        user = User.objects.get(pk=token.user_id)
    except Token.DoesNotExist:
        data = json.dumps({"continue": False, "error": "User has not logged in."})
        return HttpResponse(data, content_type='application/json')

    # grab user's project
    project = Project.objects.get(user=user, name=req_body['project'], algorithm=req_body['algorithm'])

    # grab dataset from user's project
    column_name = 'dataset'
    datasets = list(ProjectDataset.objects.filter(user=user, project=project).values(column_name))
    list_of_indexs = [each['index'] for each in req_body['ignored']]
    results = reformat_from_query(dataset=datasets, indexs_to_remove=list_of_indexs, column_name=column_name, algorithm=project.algorithm)

    start = int(req_body['train_on'])
    stop = int(req_body['train_against'])
    cluster_quantity = len(results['removed'])*3

    train_on = results['results'][:start]
    train_against = results['results'][-stop:]

    kmeans = KMeans(n_clusters=cluster_quantity, precompute_distances=False, random_state=1, max_iter=1000).fit(train_on)

    pred = kmeans.predict(train_against)
    prediction = list(int(each) for each in pred)
    cluster_indexs = {i: np.where(kmeans.labels_ == i)[0] for i in range(kmeans.n_clusters)}

    labels = label_centroids(clusters_indexs=cluster_indexs, original=datasets, possible_variables=results['removed'])
    user_labels = user_labeled_centroids(labels['centroids'], req_body['renamed'])
    prediction = relabel_prediction(prediction, user_labels)
    relabeled_accuracy = relabel_accuracy(labels['accuracy'], req_body['renamed'])

    data = json.dumps({"results":prediction, "accuracy": relabeled_accuracy, "centroids": user_labels, "project": req_body['project'], "cluster_amount": cluster_quantity, "algorithm": req_body['algorithm']})
    return HttpResponse(data, content_type='application/json')



def relabel_accuracy(accuracy, user_labels):
    new_dict = dict()
    for ind, val in enumerate(accuracy):
        new_dict[ind] = {}
        new_dict[ind]['total'] = 0

        # Used to generate the total per centroid of each answer starting with 0 for count on next loop
        for index, quantity in enumerate(accuracy[ind]):
            new_dict[ind]['total'] += accuracy[ind][quantity]
            for each in user_labels:
                if each['value'] == quantity:
                    new_dict[ind][each['renamed']] = 0

        # Used to create percentage of majority variable from total for accuracy
        for letter, quantity in enumerate(accuracy[ind]):
            for each in user_labels:
                if quantity == each['value']:
                    new_dict[ind][each['renamed']] = round((int(accuracy[ind][quantity]) / int(new_dict[ind]['total'])* 100), 2)

    # print("\nresults: {}\n".format(new_dict))
    return new_dict



def relabel_prediction(prediction, user_labels):
    new_list = list()
    for pred in prediction:
        new_list.append(user_labels[pred])

    return new_list


def user_labeled_centroids(labels, user_labels):
    for i in range(len(labels)):
        for p in range(len(user_labels)):
            if labels[i] in user_labels[p]['value']:
                labels[i] = user_labels[p]['renamed']
                
    return labels


def label_centroids(clusters_indexs, original, possible_variables):
    val_count = {}
    index_set = set()
    accuracy_count = {}

    # Iterate over cluster indexs for labeling centroids
    for index in clusters_indexs:
        val_count[index] = {}

        for i in range(len(possible_variables)):
            val_count[index][possible_variables[i][1]] = 0
            index_set.add(possible_variables[i][0])

        for dataset_index in index_set:
            for original_index in list(clusters_indexs[index]):
                val_count[index][original[original_index]['dataset'].split(',')[dataset_index]] += 1

        accuracy_count[index] = val_count[index]
        val_count[index] = max(val_count[index], key=lambda k: val_count[index][k])

    results = {
        'accuracy': accuracy_count,
        'centroids': val_count
    }
    return results


def reformat_from_query(dataset, column_name, algorithm, indexs_to_remove=[], predict_index=[]):

    formated_list = list()
    indexs_removed = set()

    if algorithm == 'Support Vector Classification':
        y_list = list()

    for counter, one_set in enumerate(dataset):
        new_list = one_set[column_name].split(',')
        start = len(new_list) - 1

        if algorithm == 'Support Vector Classification':
            new_y_list = list()

        for i in range(start, -1, -1):
            if i in indexs_to_remove:
                del new_list[i]
            else:
                if algorithm == 'Nearest Neighbor':
                    try:
                        new_list[i] = float(new_list[i])
                    except ValueError:
                        if new_list[i] == '?':
                            indexs_removed.add((i, "Question Mark"))
                        else:
                            indexs_removed.add((i, new_list[i]))
                        del new_list[i]

                elif algorithm == 'Support Vector Classification':
                    if i in predict_index:
                        new_y_list.append(new_list[i])
                        del new_list[i]
                    else:
                        try:
                            new_list[i] = float(new_list[i])
                        except ValueError:
                            pass

        if algorithm == 'Support Vector Classification':
            y_list.append(new_y_list)

        formated_list.append(new_list)

    if algorithm == 'Nearest Neighbor':
        results = {
            "results": formated_list,
            "removed": list(indexs_removed)
        }
    elif algorithm == 'Support Vector Classification':
        results = {
            "results": formated_list,
            "y_list": y_list
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

    if req_body['algorithm'] == 'Nearest Neighbor':
        formated = format_for_kmeans(list_of_data, user, new_project)
    elif req_body['algorithm'] == 'Support Vector Classification':
        formated = format_for_svc(list_of_data, user, new_project)

    # This will be used to determine which algorithm will fit their dataset based off of amount of numbers per set.
    go_on = True
    percentage = percentage_of_numbers(formated['sample_set'])

    if req_body['algorithm'] == 'Nearest Neighbor':
        if percentage > 0.75:
            data = json.dumps({
                "sample_set":formated['sample_set'],
                "indexs": formated['ignored_values'],
                "continue": go_on,
                "amount": formated['dataset_quantity'],
                "algorithm": req_body['algorithm'],
                "project": req_body['project']
            })
        else:
            go_on = False
            data = json.dumps({"continue": go_on, "error": "Please Choose another algorithm for this dataset."})

    elif req_body['algorithm'] == 'Support Vector Classification':

        data = json.dumps({
            "sample_set":formated['sample_set'],
            "indexs": [],
            "continue": go_on,
            "amount": formated['dataset_quantity'],
            "algorithm": req_body['algorithm'],
            "project": req_body['project']
        })

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


def format_for_kmeans(list_of_data, user, new_project):
    ignored_values = set()

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
                    if value == '?':
                        go_on = False
                        data = json.dumps({"continue": go_on, "error": "Currently Not Accounting for '?' with Nearest Neighbor. Please Choose a different Dataset or Algorithm. We Apologize for the inconvienence."})
                        return HttpResponse(data, content_type='application/json')
                    else:
                        new_tuple = (index, value)
                    ignored_values.add(new_tuple)

        if append:
            dataset_quantity = dataset_quantity + 1
            new_string = ','.join(str(value) for value in new_list)
            dataset = ProjectDataset(user=user, project=new_project, dataset=new_string)
            dataset.save()
        if counter == 1:
            sample_set = new_list

    results = {
        "sample_set": sample_set,
        "dataset_quantity": dataset_quantity,
        "ignored_values": list(ignored_values)
    }
    return results


####################### This is where you left off for creating svc routing ###########################
####################### This is where you left off for creating svc routing ###########################
####################### This is where you left off for creating svc routing ###########################
def format_for_svc(list_of_data, user, new_project):
    preprocess_words = set()

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
                    new_list[index] = value
                    preprocess_words.add(value)

        if append:
            dataset_quantity = dataset_quantity + 1
            new_string = ','.join(str(value) for value in new_list)
            dataset = ProjectDataset(user=user, project=new_project, dataset=new_string)
            dataset.save()
        if counter == 1:
            sample_set = new_list

    results = {
        "sample_set": sample_set,
        "dataset_quantity": dataset_quantity,
        "preprocess_words": list(preprocess_words)
    }
    return results
####################### This is where you left off for creating svc routing ###########################
####################### This is where you left off for creating svc routing ###########################
####################### This is where you left off for creating svc routing ###########################


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


@csrf_exempt
def delete_project(request):
    req_body = json.loads(request.body.decode())

    try:
        token = Token.objects.get(key=req_body['token'])
        user = User.objects.get(pk=token.user_id)

    except Token.DoesNotExist:
        data = json.dumps({"continue": False, "error": "User has not logged in."})
        return HttpResponse(data, content_type='application/json')

    project = Project.objects.get(user=user, name=req_body['project'])

    data = json.dumps({"continue": True, "project": project.name, "algorithm": project.algorithm})

    project.delete()

    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def my_project(request):

    req_body = json.loads(request.body.decode())
    print("\n\n\nreq_body?: {}\n\n".format(req_body))

    try:
        token = Token.objects.get(key=req_body['token'])
        user = User.objects.get(pk=token.user_id)

    except Token.DoesNotExist:
        data = json.dumps({"continue": False, "error": "User has not logged in."})
        return HttpResponse(data, content_type='application/json')

    project = Project.objects.get(user=user, name=req_body['project'])

    column_name = 'dataset'
    datasets = list(ProjectDataset.objects.filter(user=user, project=project).values(column_name))

    results = reformat_from_query(dataset=datasets, column_name=column_name, algorithm=project.algorithm)

    if project.algorithm == 'Nearest Neighbor':
        data = json.dumps({"continue": True, "sample_set": results['results'][0], "indexs": results['removed'], "amount": len(results['results']), "project": project.name, "algorithm": project.algorithm})

    elif project.algorithm == 'Support Vector Classification':
        data = json.dumps({"continue": True, "sample_set": results['results'][0], "amount": len(results['results']), "project": project.name, "algorithm": project.algorithm})

    return HttpResponse(data, content_type='application/json')