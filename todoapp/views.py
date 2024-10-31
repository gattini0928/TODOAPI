from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .mongo_models import *
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime
from django.views.generic import FormView
from .validators.form_validators import *
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import SignupForm

def homepage(request):
    return render(request, 'homepage.html')

def add_task(request):
    if request.method == 'POST':
        data = request.POST.dict()
        if data:
            task_name = data.get('name')
            category = data.get('category')
            priority = float(data.get('priority', 0)) # Default Value 0
            created_at = datetime.now()
            due_date_str = data.get('due_date')
            status = data.get('status') or 'Pending'
            user_id = request.user.id

            due_date = None
            if due_date_str and isinstance(due_date_str, str):
                try:
                    due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
                except ValueError:
                    messages.error(request, 'Invalid format for due_date. Use YYYY-MM-DD.')
                    return redirect('homepage') 
            else:
                due_date = due_date_str
            todo = TodoManager()
            try:
                todo.add_task(user_id, task_name, category, priority, created_at, due_date, status)
                messages.success(request, f'Task {task_name} created successfully!')
                return redirect('homepage')
            except Exception as e:
                messages.error(request,f'Failed to add a task: {str(e)}')
                return redirect('homepage')

    return render(request,'homepage.html')

def remove_task(request):
    todo = TodoManager()
    if request.method == 'POST':
        data = request.POST.dict()
        if data:
            task_name = data.get('name')
            if not todo.task_exists(task_name):
                messages.error(request, 'Task do not exists')
                return redirect('homepage')
        else:
            messages.error(request, 'No task name provided')
            return redirect('homepage')
        count_todos = todo.check_len_db()
        if count_todos:
            try:
                todo.remove_task(task_name, request.user.id)
                messages.success(request,f'Task {task_name} removed successfully')
                return redirect('homepage')
            except Exception as e:
                messages.error(request,f'Failed to remove a task: {str(e)}')
                return redirect('homepage')
    return render(request, 'homepage.html')

def finish_task(request, id):
    todo = TodoManager()
    try:
        todo.finish_task(id, request.user.id)
        messages.success(request, "Task finish with success.")
    except Exception as e:
        messages.error(request, f"Erro finish task: {str(e)}")

    return redirect('todopainel')


def todopainel(request):
    todo = TodoManager()
    tasks = todo.tasks_list(request.user.id)
    context = {'tasks':tasks}
    return render(request, 'todopainel.html', context)

def signin(request):
    if request.method == 'POST':
        data = request.POST.dict()
        email = data.get('email')
        password = data.get('password')
        print(data)
        if data:
            try:
                user = authenticate(username=email, password=password)
                if user is not None:
                    messages.success(request,f'Login successfull {user.username}')
                    login(request, user)
                    return redirect('homepage')
                else:
                    messages.error(request,f'User or password invalid')
                    return redirect('signin')
            except ValidationError as e:
                messages.error(request, e.message)
                return redirect('signin')
            
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        data = request.POST.dict()
        name = data.get('name')
        cpf = data.get('cpf')
        email = data.get('email')
        password = data.get('password')
        print(data)
        if data:
            try:
                validate_name(name)
                validate_cpf(cpf)
                validate_name(email)
                validate_password(password)

                if User.objects.filter(username=email).exists():
                    messages.error(request, 'User already exists')
                    return redirect('signup')
                else:
                    user = User.objects.create_user(username=email, password=password)
                    user.save()
                    user = authenticate(username=email, password=password)
                    todo_user = UserProfile.objects.create(name=name, email=email, cpf=cpf)
                    todo_user.save()
                    login(request,user)
                    messages.success(request, 'User created with success')
                    return redirect('homepage')
            except ValidationError as e:
                messages.error(request, e.message)
                return redirect('signup')
            
    return render(request, 'signup.html')

@login_required
def logout(request):
    user = request.user
    logout(user)
    return redirect('homepage')