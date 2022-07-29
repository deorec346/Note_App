import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
pytestmark = pytest.mark.django_db


class TestUser:

    @pytestmark
    def test_user_signup(self, client, user_data):
        user_model = get_user_model()
        assert user_model.objects.count() == 0
        temp_url = reverse("register_api")
        resp = client.post(temp_url, data=user_data)
        assert user_model.objects.count() == 0
        assert resp.status_code == 400

    @pytestmark
    def test_user_login(self, client, user_data, create_user):
        user_model = get_user_model()
        assert user_model.objects.count() == 1
        url = reverse("login_api")
        response = client.post(url, user_data)
        assert response.status_code == 200

    @pytestmark
    def test_login_fail(self, client):
        url = reverse('login_api')
        login_data = {'username': 'Ravi123', 'password': 'Pass@13'}
        respone = client.post(url, login_data)
        assert respone.status_code == 401
