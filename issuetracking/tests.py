import pytest
import uuid
from django.urls import reverse
from django.test import Client
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token



from .models import Project, Issue, Comment, Contributor
from account.models import User


@pytest.fixture
def client(db):
    return APIClient()


   
def test_api_jwt(client):
    
    url = reverse('token_obtain_pair')
    u = User.objects.create_user(username='user', email='user@foo.com', password='pass')
    u.is_active = False
    u.save()

    resp = client.post(url, {'email':'user@foo.com', 'password':'pass'}, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    u.is_active = True
    u.save()

    resp = client.post(url, {'username':'user@foo.com', 'password':'pass'}, format='json')
    assert resp.status_code == status.HTTP_200_OK
    assert 'token' in resp.data
    token = resp.data['token']
    print('*********************', token)

    verification_url = reverse('token_refresh')
    resp = client.post(verification_url, {'token': token}, format='json')
    assert resp.status_code == status.HTTP_200_OK

    resp = client.post(verification_url, {'token': 'abc'}, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='JWT ' + 'abc')
    resp = client.get('/projects/', data={'format': 'json'})
    assert resp.status_code == status.HTTP__UNAUTHORIZED
    client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
    resp = client.get('/projects/', data={'format': 'json'})
    assert resp.status_code == status.HTTP_200_OK