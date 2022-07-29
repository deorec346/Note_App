import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .models import Note
from .serializers import NoteSerializer
from .utils import verify_token, RedisOperation
logging.basicConfig(filename="views.log", filemode="w")


class Notes(APIView):
    @verify_token
    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            RedisOperation().add_note(request.data.get("user_id"), note=serializer.data)
            return Response(
                {
                    "message": "Data store successfully",
                    "data": serializer.data
                }, 201)
        except Exception as e:
            logging.error(e)
            return Response({
                "message": str(e)
            }, 400)

    @verify_token
    def get(self, request):
        try:
            data = RedisOperation().get_note(user_id=request.data.get("user_id")).values()
            if len(data) != 0:
                return Response({
                    "message": "note found",
                    "data": data
                }, 200)
            return Response({
                "message": "empty note in redis"
            }, 400)
        except Exception as e:
            return Response({
                "message": str(e),
            }, 400)

    @verify_token
    def delete(self, request, pk):
        try:
            note = Note.objects.get(pk=pk)
            is_deleted = RedisOperation().delete_note(request.data.get("user_id"), pk)
            note.delete()
            if is_deleted is False:
                return Response({
                    "message": "note not found"
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "message": "note delete successfully"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logging.error(e)
            print(e)
            return Response(
                {
                    "message": "Data not deleted"
                },
                status=status.HTTP_400_BAD_REQUEST)


    @verify_token
    def put(self, request):

        note = Note.objects.get(pk=request.data["note_id"])
        serializer = NoteSerializer(note, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            RedisOperation().update_note(serializer.data)
            return Response({
                "message": "user update successfully",
                "data": serializer.data
            }, 200)
        except ObjectDoesNotExist:
            return Response({
                "message": "note not found"
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e)
            print(e)
            return Response(
                {
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST)