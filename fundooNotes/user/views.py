import json
import logging
from django.contrib.auth.models import auth
from django.http import JsonResponse

from user.models import User

logging.basicConfig(filename="views.log", filemode="w")


def login(request):
    try:
        if request.method == "POST":
            user_dict = json.loads(request.body)
            user = auth.authenticate(username=user_dict.get("username"), password=user_dict.get("password"))
            if user is not None:
                return JsonResponse({
                    "message": "user login successfully",
                    "data": {
                        "username": user.username
                    }
                })
            return JsonResponse({
                "message": "user login unsuccessful"
            })
    except Exception as e:
        logging.error(e)
        return JsonResponse({
            "message": str(e)
        })


def user_register(request):
    try:
        if request.method == "POST":
            user_dict = json.loads(request.body)
            username = user_dict.get('username')
            User.objects.create_user(username=username,
                                     password=user_dict.get('password'),
                                     age=int(user_dict.get('age')),
                                     email=user_dict.get('email'), phone=user_dict.get('phone'))
            return JsonResponse({"message": "user register successful"})
    except Exception as e:
        logging.error(e)
        return JsonResponse({"message": str(e)})
