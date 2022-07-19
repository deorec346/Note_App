import pytest
import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from note.models import Note


class TestNote:
    @pytest.mark.django_db
    def test_add_note(self, client, note_data, create_user,update_note_data):
        user_model = get_user_model()
        assert user_model.objects.count() == 1

        # add note
        url = reverse("note_api")

        response = client.post(url, note_data, content_type='application/json')
        assert response.status_code == 201
        user1 = user_model.objects.get(id=1)
        assert user1.id == 1

        # get note
        url = reverse('note_id_id', kwargs={'note_id_id': response.data['data']['note_id']})
        response = client.get(url)
        assert response.data["message"] == "note found"
        assert response.status_code == 200

        # update note
        url = reverse('note')
        response = client.put(url, update_note_data, content_type='application/json')
        assert response.data['data']['title'] == update_note_data.get('title')
        assert response.status_code == 200

        # delete note
        url = reverse('gd_note', kwargs={'id': response.data['data']['id']})
        response = client.delete(url, CONTENT_TYPE='application/json')
        assert Note.objects.count() == 0
        assert response.status_code == 204
















































# import pytest
# from faker import Faker
# from rest_framework.reverse import reverse
#
# from note.models import Note
# from user.models import User
#
# faker = Faker()
# REGISTER_URL = reverse('register_api')
# LOGIN_URL = reverse('login_api')
#
#
# @pytest.fixture
# def create_user():
#     return User.objects.create_user(username="Ravi123", email="deorec346@gmail.com", password="Pass@123", age= 25, phone=937070)
#
#
# class TestUser:
#
#     def test_user_cannot_register_with_no_data(self, client):
#         res = client.post(REGISTER_URL)
#         assert res.status_code == 400
#
#     def test_user_register_correctly(self, client, db):
#         user_data = {
#             "username": "Ravi123",
#             "password": "Pass@1234",
#             "age": 25,
#             "email": "ravi@gmail.com",
#             "phone": 937070
#         }
#         res = client.post(REGISTER_URL, user_data, format="json")
#         assert res.data['data']['email'] == user_data['email']
#         assert res.data['data']['username'] == user_data['username']
#         assert res.status_code == 201
#
#
# NOTE_URL = reverse('note_api')
#
#
# class TestNote:
#
#     def test_note_cannot_register_with_no_data(self, client):
#         res = client.post(NOTE_URL)
#         assert res.status_code == 400
#
#     def test_note_create_correctly(self, client, db, create_user):
#         note_data = {
#             'user_id': create_user.id,
#             "title": "Think and Grow Rich",
#             "description": "Think and Grow Rich is Napoleon Hill's most popular book, summarizing his Philosophy of Success and explaining it for the general public. The only version of the book we at the Napoleon Hill Foundation currently recommend is Think and Grow Rich: The Original 1937 Unedited Edition. This edition is a reproduction of Napoleon Hill’s personal copy of the first edition, printed in March of 1937.",
#             "note_id": "4",
#             "created_at": "10/05/1937",
#             'is_archive': True,
#         }
#         response = client.post(NOTE_URL, note_data, format="json")
#
#         assert response.data['data']['user_id'] == create_user.id
#         assert response.data['data']['title'] == note_data['title']
#         assert response.data['data']['description'] == note_data['description']
#         assert response.data['data']['note_id'] == note_data['note_id']
#         assert response.data['data']['created_at'] == note_data['created_at']
#
#         assert response.status_code == 201