from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from models import User, Poke
from django.db.models import Count

# Create your views here.
def index(request):
    if 'user' in request.session:
        return redirect('/pokes')
    return render(request, 'exam_app/index.html')



def register(request):
    result = User.objects.validateReg(request)
    if result[0] == False:
        print_messages(request, result[1])
        return redirect(reverse ('index'))
    return log_user_in(request, result[1])


def login(request):
    result = User.objects.validateLogin(request)
    if result[0] == False:
        print_messages(request, result[1])
        return redirect(reverse ('index'))
    return log_user_in(request, result[1])

def print_messages(request, message_list):
    for message in message_list:
        messages.add_message(request, messages.INFO, message)

def log_user_in(request, user):
    userobject = User.objects.get(email=user.email)
    userid = userobject.id
    request.session['user'] = {
    'id' : userid,
    'name' : user.alias,
    }
    return redirect('/pokes')

def logout(request):
    request.session.pop('user')
    return redirect(reverse('index'))

def pokes(request):
    if 'user' not in request.session:
        errors = ["You must register/log in to access the site!"]
        return render(request, 'exam_app/index.html', context={'hacks': errors})
    id = request.session['user']['id']
    user = User.objects.get(id=id)
    # Gets all users but the current user
    allButMe = User.objects.exclude(id=id)
    # Gets all poke objects where user was poked
    allPokesOnMe = Poke.objects.filter(pokedUser = user)
    # Count of people who have poked user
    PeopleWhoPokedMeCount = allButMe.filter(user_who_poked__in=allPokesOnMe).distinct().count()
    # Get all user objects who poked user append count of own pokes
    PeopleWhoPokedMe = allButMe.filter(user_who_poked__in=allPokesOnMe).annotate(total_pokes=Count('id')).order_by('-total_pokes')
    allPokesButMine = allButMe.annotate(total_pokes=Count('poked_user'))

    return render(request, 'exam_app/pokes.html', context={'users': allPokesButMine, 'PeopleWhoPokedMeCount': PeopleWhoPokedMeCount, 'PeopleWhoPokedMe': PeopleWhoPokedMe})


def pokeUser(request, id):
    user_id = request.session['user']['id']
    Poke.objects.poke(user_id, id)
    return redirect('/pokes')
