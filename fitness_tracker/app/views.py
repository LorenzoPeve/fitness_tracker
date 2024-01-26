from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import User
from . import database

def index(request):
    if request.user.is_authenticated:
        return render(request, 'app/home.html')
    else:
        return render(request, 'app/welcome.html')


@login_required
def add_exercise(request):
    return render(request, 'app/add_exercise.html')

def dbtest(request):

    conn = database.get_db()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM records;""")
    print(cur.fetchone())
    return render(request, 'app/add_exercise.html')


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
 