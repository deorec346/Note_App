import json
import logging
from rest_framework.response import Response

from fundooNote.rediscode import RedisCode
from user.utils import EncodeDecode
from functools import wraps
logging.basicConfig(filename="view.log", filemode="w")

# logger = logging.getLogger(__name__)


def verify_token(function):
    """
        creating function to verify token
    """
    @wraps(function)
    def wrapper(self, request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            logging.error('Token not provided in the header')
            return Response({"message": 'Token not provided in the header'}, status=400)

        token = request.META['HTTP_AUTHORIZATION']
        id = EncodeDecode().decode_token(token)
        request.data.update({'user_id': id.get("user_id")})
        return function(self, request)

    return wrapper


class RedisOperation:

    def __init__(self):
        self.redis_obj = RedisCode()

    def get_note(self, user_id):
        """
        for geting note from cache
        :param user_id: user_id
        :return:
        """
        try:
            data = self.redis_obj.get(user_id)
            if data is None:
                return None
            return json.loads(data)
        except Exception as e:
            logging.error(e)
            raise e

    def add_note(self, user_id, note):
        """
        Adding note to cache
        :param user_id: user_id
        :param note: note details
        :return:
        """
        try:
            existing_note = self.get_note(user_id)
            if existing_note is None:
                note_data = {int(note.get('id')): note}
            else:
                new_note = {int(note.get('id')): note}
            note_data.update({int(note.get('id')): note})
            self.redis_obj.set(user_id, json.dumps(note_data))
        except Exception as e:
            logging.error(e)

    def delete_note(self, user_id, note_id):
        """
        deleting note to cache
        :param user_id:
        :param note_id:
        :return:
        """

        try:
            note_dict = json.loads(self.redis_obj.get(user_id))
            if note_dict.get(str(note_id)):
                note_dict.pop(str(note_id))
                self.redis_obj.set(user_id, json.dumps(note_dict))
        except Exception as e:
            logging.error(e)

    def update_note(self, note):
        """
        updating note to cache
        :param note:note details
        :return:
        """
        try:
            user_id = note.get('user_id')
            id = str(note.get("id"))
            note_dict = json.loads(self.redis_obj.get(user_id))

            if note_dict.get(id):
                note_dict.update({id: note})
                self.redis_obj.set(user_id, json.dumps(note_dict))
            else:
                print("id not found")

        except Exception as e:
            logging.error(e)