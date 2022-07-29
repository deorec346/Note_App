import pytest
from rest_framework.reverse import reverse
from note.models import Note
NOTE_URL = reverse('note_api')


@pytest.fixture
def create_user(django_user_model, db):
    return django_user_model.objects.create_user(username="chetan2122",email="deorec@gmail.com", password="Pass@123", age=25, phone=937070)


@pytest.fixture
def headers(create_user, client, db):
    payload = {'username': "chetan2122", 'password': "Pass@123",
    }

    response = client.post(reverse('login_api'), payload)
    token = response.data['data']['token']
    return {'HTTP_AUTHORIZATION': token, 'content_type': 'application/json'}


class TestNote:

    def test_note_cannot_register_with_no_data(self, client, headers):
        res = client.post(NOTE_URL, **headers)
        assert res.status_code == 200

    def test_note_create_correctly(self, client, db, create_user, headers):
        note_data = {
            'user_id': create_user.id,
            'title': "The secret",
            'description': "This is new notes",
            'date_joined'
            'is_archive': True,
        }
        response = client.post(NOTE_URL, note_data, **headers)

        assert response.data['data']['user_id'] == create_user.id
        assert response.data['data']['title'] == note_data['title']
        assert response.data['data']['description'] == note_data['description']
        assert response.status_code == 201

    def test_note_update_correctly(self, client, db, create_user, headers):
        note_data = {
            'user_id': create_user.id,
            'title': "The secret",
            'description': "This is new notes",
            'is_archive': True,
        }
        res = client.post(NOTE_URL, note_data, **headers)
        note_id = res.data['data']['id']
        updated_note_data = {
            'note_id': note_id,
            'title': "The real World",
            'description': "This is new notes",
            'is_archive': True,
        }
        response = client.put(NOTE_URL, updated_note_data, **headers)
        assert response.data['data']['title'] == updated_note_data.get('title')
        assert response.status_code == 202

    def test_note_delete_correctly(self, client, db, create_user, headers):
        note_data = {
            'title': "The secret",
            'description': "This is new notes",
            'is_archive': True,
        }

        response = client.post(NOTE_URL, note_data, **headers)
        note_id = response.data['data']['user_id']
        res = client.delete(NOTE_URL, {'note_id': note_id}, **headers)

        assert res.status_code == 400

    def test_note_get_correctly(self, client, db, create_user, headers):
        note_data = {
            'title': "The secret",
            'description': "This is new notes",
            'is_archive': True,
        }
        response = client.post(NOTE_URL, note_data, **headers)
        note_id = response.data['data']['user_id']

        response = client.delete(NOTE_URL, {"note_id": note_id}, **headers)
        assert Note.objects.count() == 1
        assert response.status_code == 400
