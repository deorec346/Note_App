from django.urls import path
from note import views

urlpatterns = [
    path('note', views.Notes.as_view(), name='note_api'),
    # path('note/<int:id>', views.Notes.as_view(), name='note')

]