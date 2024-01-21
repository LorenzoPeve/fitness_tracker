from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logexercise", views.add_exercise, name="add_exercise")
]
