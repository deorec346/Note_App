import logging
from django.contrib.auth.models import auth
from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from user.models import User
from user.serializers import UserSerializer
from rest_framework.views import APIView
from .utils import EncodeDecode
from jwt import ExpiredSignatureError, DecodeError
logging.basicConfig(filename="views.log", filemode="w")


class UserRegistration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = User.objects.create_user(**request.data)
            token = EncodeDecode().encode_token({"id": user.pk})
            url = "http://127.0.0.1:8000/user/validate/" + str(token)
            send_mail("register", url, 'deorec346@gmail.com', [serializer.data['email']], fail_silently=False)
            return Response({"message": "data store successfully", "data": {"username": serializer.data}})

        except Exception as e:
            logging.error(e)
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            users = User.objects.get(username=request.data.get("username"))
            serializer = UserSerializer(users)
            return Response({
                "message": "user found",
                "data": serializer.data
            })
        except ObjectDoesNotExist:
            return Response({
                "message": "user not found"
            }, 200)

        except Exception as e:
            return Response({
                "error_message": str(e)
            }, 400)


class UserLogin(APIView):

    def post(self, request):
        """
            login existing user with username and password
        """
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                token = EncodeDecode().encode_token(payload={"user_id": user.pk})
                return Response({"message": "login successful", "data": {"token": token}}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "user login unsuccessful", "data": {}}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ValidateToken(APIView):

    def get(self, request, token):
        """
            Checking existing token whether it is valid or expired
        """
        try:
            decode_token = EncodeDecode().decode_token(token=token)
            user = User.objects.get(id=decode_token.get('id'))
            user.is_verified = True
            user.save()
            return Response({"message": "Validate Successfully", "data": user.pk},
                            status=status.HTTP_201_CREATED)
        except ExpiredSignatureError:
            return Response({"message": "token expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except DecodeError:
            return Response({"message": "wrong token"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)