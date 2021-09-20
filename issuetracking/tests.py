import pytest
from rest_framework.test import APIClient

from .models import Project, Issue, Comment, Contributor
from account.models import User

###########################################################################
###############################  FIXTURES  ################################
###########################################################################

@pytest.fixture
def client(db):
    return APIClient()

@pytest.fixture
def user1(client: APIClient):
    response = client.post('/signup/',
                {'username': 'azalae',
                'first_name': 'elo',
                'last_name': 'dalb',
                'email': 'elo@soleneidos.fr',
                'password': 'choucroute'})
    response = client.post('/login/',
                          {'username': 'azalae',
                           'password': 'choucroute'})
    return response.data['access']

@pytest.fixture
def user2(client: APIClient):
    response = client.post('/signup/',
                {'username': 'LukeSkywalker',
                'first_name': 'Luke',
                'last_name': 'Skywalker',
                'email': 'luke@soleneidos.fr',
                'password': 'EtoileNoire'})
    response = client.post('/login/',
                          {'username': 'LukeSkywalker',
                           'password': 'EtoileNoire'})
    return response.data['access']

@pytest.fixture
def user1_project(client: APIClient, user1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    return client.post('/projects/', {
        'title': 'Premier projet',
        'description': 'Voilà bien le premier projet test',
        'type': 'BACK'}, format='json')

@pytest.fixture
def user1_issue_project(client: APIClient, user1, user1_project, user2):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    return client.post('/projects/1/issues/', {
        'title': 'Premier problème',
        'description': "problème 1 du projet 1",
        'tag': 'BUG',
        'priority': 'LOW',
        'status': 'TODO',
        'assignee_user': 'LukeSkywalker'})

@pytest.fixture
def user1_comment_issue_project(client: APIClient,
                                user1,
                                user1_issue_project):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    return client.post('/projects/1/issues/1/comments/', {
        'description': "commentaire 1 au problème 1 du projet 1"})

#############################################################################
############################  Tests PROJECTS  ###############################
#############################################################################

def test_get_project_list(client, user1, user1_project):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    response = client.get('/projects/')
    assert response.status_code == 200


def test_post_new_project(client, user1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    response = client.post('/projects/', {
        'title': 'Premier projet',
        'description': 'Voilà bien le premier projet test',
        'type': 'BACK'}, format='json')
    assert response.status_code == 201


def test_get_project1(client, user1, user1_issue_project):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    response = client.get('/projects/1/')
    assert response.status_code == 200

############################################################################
###########################  Tests ISSUES  #################################
############################################################################

def test_issues_post(client, user1, user1_project, user2):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    response = client.post('/projects/1/issues/', {
        'title': 'Premier problème',
        'description': "problème 1 de l'issue 1",
        'tag': 'BUG',
        'priority': 'LOW',
        'status': 'TODO',
        'assignee_user': 'LukeSkywalker'})
    assert response.status_code == 201


def test_get_issue1_project1(client, user1, user1_issue_project):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    response = client.get('/projects/1/issues/1/')
    assert response.status_code == 200

############################################################################
############################# Tests COMMENTS  ##############################
############################################################################

def test_comment_post(client, user1, user1_issue_project, user2):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    response = client.post('/projects/1/issues/1/comments/', {
        'description': 'Premier commentaire'})
    assert response.status_code == 201

def test_get_comment1_issue1_project1(client,
                                      user1,
                                      user1_comment_issue_project):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user1)
    response = client.get('/projects/1/issues/1/comments/1/')
    assert response.status_code == 200
