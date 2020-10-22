from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.


def index(request):
    return render(request, 'index.html')


def addUser(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        # check if the errors dictionary has anything in it
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')

        user = User.objects.filter(email=request.POST['email'])
        if len(user) > 0:
            messages.error(request, "Email is already in use.",
                           extra_tags="email")
            return redirect('/')

        pw = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()

        User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw
        )
        request.session['user_id'] = User.objects.last().id
        return redirect('/thoughts')
    else:
        return redirect('/')


def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')

        user = User.objects.filter(email=request.POST['login_email'])
        if len(user) == 0:
            messages.error(request, "Invalid Email/Password.",
                           extra_tags="login")
            return redirect('/')

        if not bcrypt.checkpw(request.POST['login_pw'].encode(), user[0].password.encode()):
            messages.error(request, "Invalid Email/Password.",
                           extra_tags="login")
            return redirect('/')

        request.session['user_id'] = user[0].id
        return redirect('/thoughts')
    else:
        return redirect('/')


def thoughts(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'all_the_thoughts': Thought.objects.all().order_by('-likes')        }
        return render(request, 'thoughts.html', context)


def logout(request):
    request.session.clear()
    return redirect('/')


def addThought(request):
    if request.method == "POST":
        errors = Thought.objects.thought_validator(request.POST)
        # check if the errors dictionary has anything in it
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/thoughts')
        Thought.objects.create(
        thought=request.POST['thought'],
        user=User.objects.get(id=request.POST['user_id'])
    )
    return redirect('/thoughts')


def thoughtInfo(request, thought_id):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'one_thought': Thought.objects.get(id=thought_id),
        'one_like': Thought.objects.filter(user_id=request.session['user_id'] ),
        'id': request.session['user_id'],
    }
    return render(request, 'thoughtInfo.html', context)


def destroyThought(request, thought_id):
    thought_to_destroy = Thought.objects.get(id=thought_id)
    thought_to_destroy.delete()
    return redirect('/thoughts')


def likes(request, user_id, thought_id):
    one_user = User.objects.get(id=user_id)
    one_thought = Thought.objects.get(id=thought_id)
    one_thought.likes.add(one_user)
    return redirect('/thoughts/'+str(thought_id))

def unlikes(request, user_id, thought_id):
    one_user = User.objects.get(id=user_id)
    one_thought = Thought.objects.get(id=thought_id)
    one_thought.likes.remove(one_user)
    return redirect('/thoughts/'+str(thought_id))
