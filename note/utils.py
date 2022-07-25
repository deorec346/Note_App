import logging
from rest_framework.response import Response
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