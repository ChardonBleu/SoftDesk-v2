import pytest
from rest_framework.test import APIClient

from .models import User


@pytest.fixture
def api_client(db):
    return APIClient()


# ################################################################# #
# ####################### TEST registration ####################### #


def test_registration(db, api_client: APIClient):
    user_count = User.objects.count()
    response = api_client.post('/signup/',
                               {'username': 'azalae',
                                'first_name': 'elo',
                                'last_name': 'dalb',
                                'email': 'elo@soleneidos.fr',
                                'password': 'choucroute'})
    assert response.status_code == 201
    assert User.objects.count() == user_count + 1
