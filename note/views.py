import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from .models import Note
from .serializers import NoteSerializer
from .utils import verify_token
logging.basicConfig(filename="views.log", filemode="w")


class Notes(APIView):

    @verify_token
    def post(self, request):
        """
        Registering note
        """
        serializer = NoteSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "message": "note store successfully",
                    "data": serializer.data
                }, 201)

        except ValidationError:
            return Response({
                'message': serializer.errors
            })

        except Exception as e:
            logging.error(e)
            return Response({'message': str(e)})

    @verify_token
    def get(self, request):
        """
            Displaying note details
        """
        try:
            note = Note.objects.filter(user_id=request.data.get('id'))
            serializer = NoteSerializer(note, many=True)
            return Response({"message": "note found", "data": serializer.data}, status=status.HTTP_200_OK)
        except note.DoesNotExist as dne:
            return Response({"message": "note not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def delete(self, request):
        """
            Deleting particular note
        """
        try:
            Note.objects.get(id=request.data.get("note_id")).delete()
            return Response({
                "message": "note delete successfully",

            }, 204)

        except ObjectDoesNotExist:
            return Response({
                "message": "note not found"
            }, 400)

        except Exception as e:
            logging.error(e)
            return Response({
                "message": str(e)
            }, 400)

    @verify_token
    def put(self, request):
        """
             Creating note view and performing crud operation
         """

        global serializer
        try:
            note = Note.objects.get(pk=request.data.get("note_id"))
            serializer = NoteSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "message": "user update successfully",
                "data": serializer.data
            }, status.HTTP_202_ACCEPTED)

        except ObjectDoesNotExist:
            return Response({
                "message": "note not found"
            }, 400)

        except ValidationError as ve:
            logging.error(ve)
            return Response({
                'message': serializer.error
            }, 400)

        except Exception as e:
            return Response({
                'message': str(e)
            }, 400)