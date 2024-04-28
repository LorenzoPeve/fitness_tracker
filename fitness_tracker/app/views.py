from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
import psycopg2

from .models import User
from . import database


def index(request):
    if request.user.is_authenticated:
        return render(request, 'app/home.html')
    else:
        return render(request, 'app/welcome.html')

def test(request):
    print(request)
    return "hello world"

def login_view(request):

    if request.method == "GET":

        next_url = request.GET.get('next')
        if next_url:
            request.session['next'] = next_url
        return render(request, "app/login.html")

    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, "app/login.html", {"invalid_creds": True})
        else:       
            login(request, user)

            next_url = request.session.get('next')
            if next_url:
                # Delete 'next' from session to prevent reusing it
                del request.session['next']
                return redirect(next_url)
            else:
                return redirect("index")

def logout_view(request):
    logout(request)
    return redirect("index") 

def register(request):

    if request.method == "GET":
        return render(request, "app/register.html")

    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]

    if User.objects.filter(username=username).exists():
        return render(request, "app/register.html", {
            "invalid_message": "Username already taken."
        })

    if User.objects.filter(email=email).exists():
        return render(request, "app/register.html", {
            "invalid_message": "Email already taken."
        })

    user = User.objects.create_user(username, email, password)
    user.save()    
    login(request, user)
    return redirect("index")



@login_required
def add_exercise(request):

    if request.method == "GET":

        if 'exercises_list' not in request.session:
            exercises = database.get_user_exercises(request.user.username)
            request.session['exercises_list'] = exercises

        return render(
            request,
            "app/add_exercise.html",
            {'exercises': request.session['exercises_list']})
    try:
        if request.POST['exercise_type'] == 'weight_reps':

            for _ in range(int(request.POST['n_sets'])):

                database.add_exercise(
                    user_id = request.user.username,
                    exercise = request.POST['exercise'],
                    weight = request.POST['weight'],
                    reps = request.POST['n_reps'],
                    date = request.POST['date'],
                    after_wod = request.POST.get('is_after_wod', False),
                    comment = request.POST['activity_comments']
                )
        
        elif request.POST['exercise_type'] == 'amrap':

            database.add_amrap(
                user_id = request.user.username,
                wod = request.POST['amrap_wod'],
                timecap = request.POST['amrap_timecap'],
                rounds_plus_reps = request.POST['amrap_score'],
                date = request.POST['date'],
                comment = request.POST['activity_comments']
            )

        elif request.POST['exercise_type'] == 'emom':

            database.add_emom(
                user_id = request.user.username,
                wod = request.POST['emom_wod'],
                duration = request.POST['emom_duration'],
                date = request.POST['date'],
                comment = request.POST['activity_comments']
            )

        elif request.POST['exercise_type'] == 'cardio':

            duration = (
                float(request.POST['cardio_minutes']) + 
                float(request.POST['cardio_seconds']) / 60
            )
            database.add_cardio(
                user_id = request.user.username,
                activity = request.POST['cardio_activity'],
                distance = request.POST['cardio_distance'],
                time = duration,
                date = request.POST['date'],
                comment = request.POST['activity_comments']
            )

        elif request.POST['exercise_type'] == 'rft':

            duration = (
                float(request.POST['rft_minutes']) + 
                float(request.POST['rft_seconds']) / 60
            )
            database.add_rounds_for_time(
                user_id = request.user.username,
                wod = request.POST['rft_wod'],
                rounds = request.POST['rft_rounds'],
                time = duration,
                date = request.POST['date'],
                comment = request.POST['activity_comments']
            )
    except psycopg2.errors.CheckViolation as e:
        if "valid_amrap_score" in e.args[0]:
            return render(
                request,
                "app/add_exercise.html",
                {
                    'message': 'Invalid AMRAP score. Use [rounds]+[reps].',
                    'message_type': 'exception'
                },
            )

    except Exception as e:
        raise e
    else:
        return redirect("add_exercise_sucess")

@login_required
def add_exercise_sucess(request):
    return render(
        request,
        "app/add_exercise.html",
        {'message_type': 'success'}
    )

@login_required
def add_exercise_failure(request):
    return render(
        request,
        "app/add_exercise.html",
        {'message_type': 'exception'}
    )