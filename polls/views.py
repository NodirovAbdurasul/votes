from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse

from polls.models import Vote
from users.models import MyUser


def index(request):
    return render(request, "polls.html")


def registration(request):
    if request.method == 'POST':
        new_user = MyUser.objects.create(
            phone_number=request.POST.get('phone_number'),
        )
        new_user.set_password(request.POST.get('password'))
        new_user.save()
        return redirect('login')
    return render(request, "registration.html")


def login(request):
    if request.method == 'POST':
        user = authenticate(phone_number=request.POST.get('phone_number'),
                            password=request.POST.get('password'))
        if user:
            auth_login(request, user)
            # set user-specific data in the session
            request.session['phone_number'] = user.phone_number
            request.session.save()
            return redirect('voting', )
        else:
            return HttpResponse("Invalid user")
    return render(request, "login.html")


def votes(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            democratic_votes = Vote.objects.filter(vote_to='d').count()
            republic_votes = Vote.objects.filter(vote_to='r').count()
            return render(request, "view_votes.html", {"d": democratic_votes, "r": republic_votes})
        else:
            if request.method == 'POST':
                if request.POST.get('vote'):
                    new_vote = Vote.objects.create(
                        user=request.user,
                        vote_to='d'
                    )
                    new_vote.save()
                else:
                    new_vote = Vote.objects.create(
                        user=request.user,
                        vote_to='r'
                    )
                    new_vote.save()

                return redirect('login')
            else:
                return render(request, 'voting.html')
    else:
        return redirect('login')


def logout_view(request):
    logout(request)
    Session.objects.filter(session_key=request.session.session_key).delete()
    return redirect('login')