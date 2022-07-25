# import pytest
#
# from django.contrib.auth import get_user_model
#
#
# @pytest.fixture
# def user_data():
#     return {
#         "username": "Ravi123",
#         "password": "Pass@1234",
#         "age": 25,
#         "email": "ravi@gmail.com",
#         "phone": 937070,
#         "is_verified": 0
#     }
#
#
# @pytest.fixture
# def create_user(user_data):
#     return get_user_model().objects.create_user(**user_data)
#
#
# @pytest.fixture
# def note_data():
#     return {
#         "title": "Think and Grow Rich",
#         "description": "Think and Grow Rich is Napoleon Hill's most popular book, summarizing his Philosophy of "
#                        "Success and explaining it for the general public. The only version of the book we at the "
#                        "Napoleon Hill Foundation currently recommend is Think and Grow Rich: The Original 1937 "
#                        "Unedited Edition. This edition is a reproduction of Napoleon Hill’s personal copy of the "
#                        "first edition, printed in March of 1937.",
#         "note_id": "4",
#         "created_at": "10/05/1937"
#     }
#
#
# @pytest.fixture
# def update_note_data():
#     return {
#         "note_id": "4",
#         "title": "my update note",
#         "description": "this is my update notes",
#         "user_id": 1
#     }