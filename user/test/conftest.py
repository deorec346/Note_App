import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def user_data():
    return {
        "username": "Ravi123",
        "password": "Pass@1234",
        "age": 25,
        "email": "ravi@gmail.com",
        "phone": 937070,
        "is_verified": 0
    }


@pytest.fixture
def create_user(user_data):
    return get_user_model().objects.create_user(**user_data)
