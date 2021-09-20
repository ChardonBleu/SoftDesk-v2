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


   
