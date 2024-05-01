from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login_view"),
    path("logout", views.logout_view, name="logout_view"),
    path("register", views.register, name="register"),
    path("logexercise", views.add_exercise, name="add_exercise"),
    path("logexercise/sucess", views.add_exercise_sucess, name="add_exercise_sucess"),
    path("logexercise/error", views.add_exercise_failure, name="add_exercise_failure"),
    path("exercises", views.get_user_exercises, name="get_user_exercises"),
]
