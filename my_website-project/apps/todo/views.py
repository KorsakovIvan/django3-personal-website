from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import ToDoForm
from .models import ToDo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'todo/home.html')


def signup_user(request):
    if request.method == 'GET':
        return render(request, 'todo/signup_user.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('todo:current_todos')
            except IntegrityError:
                return render(request, 'todo/signup_user.html', {'form': UserCreationForm(),
                                                                 'error': "This username has already been taken"})
        else:
            return render(request, 'todo/signup_user.html', {'form': UserCreationForm(),
                                                             'error': "Passwords didn't match"})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'todo/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/login.html', {'form': AuthenticationForm(),
                                                       'error': "Username and password didn't match"})
        else:
            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            else:
                return redirect('todo:current_todos')


@login_required(login_url='/todo/login/')
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('todo:home')


@login_required(login_url='/todo/login/')
def create_todo(request):
    if request.method == 'GET':
        return render(request, 'todo/create_todo.html', {'form': ToDoForm()})
    else:
        try:
            form = ToDoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.assigned_to = request.user
            new_todo.save()
            return redirect('todo:current_todos')
        except ValueError:
            return render(request, 'todo/create_todo.html', {'form': ToDoForm(),
                                                             'error': 'Bad data passed in. Try again'})


@login_required(login_url='/todo/login/')
def current_todos(request):
    todos = ToDo.objects.filter(assigned_to=request.user, status='to_do')
    return render(request, 'todo/current_todos.html', {'todos': todos})


@login_required(login_url='/todo/login/')
def view_todo(request, todo_pk):
    task = get_object_or_404(ToDo, pk=todo_pk, assigned_to=request.user)
    if request.method == 'GET':
        form = ToDoForm(instance=task)
        return render(request, 'todo/todo_task.html', {'task': task, 'form': form})
    else:
        form = ToDoForm(request.POST, instance=task)
        try:
            form.save()
            return redirect('todo:current_todos')
        except ValueError:
            return render(request, 'todo/todo_task.html', {'task': task, 'form': form,
                                                             'error': 'Bad info. Please try again'})


@login_required(login_url='/todo/login/')
def complete_todo(request, todo_pk):
    task = get_object_or_404(ToDo, pk=todo_pk, assigned_to=request.user)
    if request.method == 'POST':
        task.status = 'done'
        task.completed_on = timezone.now()
        task.save()
        return redirect('todo:current_todos')


@login_required(login_url='/todo/login/')
def completed_todos(request):
    todos = ToDo.objects.filter(assigned_to=request.user, status='done').order_by('-completed_on')
    return render(request, 'todo/completed_todos.html', {'todos': todos})


@login_required(login_url='/todo/login/')
def delete_todo(request, todo_pk):
    task = get_object_or_404(ToDo, pk=todo_pk, assigned_to=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('todo:current_todos')
