from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .mongo_models import *
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime
from .forms import SignUpForm
from .validators.form_validators import *
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from .models import UserProfile
from django.http import HttpRequest

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
                    messages.add_message(request, messages.ERROR,'Invalid format for due_date. Use YYYY-MM-DD.')
                    return redirect('homepage') 
            else:   
                due_date = due_date_str
            todo = TodoManager()
            try:
                todo.add_task(user_id, task_name, category, priority, created_at, due_date, status)
                messages.add_message(request,messages.SUCCESS, f'Task {task_name} created successfully!')
                return redirect('homepage')
            except Exception as e:
                messages.add_message(request,messages.ERROR,f'Failed to add a task: {str(e)}')
                return redirect('homepage')

    return render(request,'homepage.html')

def remove_task(request):
    todo = TodoManager()
    if request.method == 'POST':
        data = request.POST.dict()
        if data:
            task_name = data.get('name')
            if not todo.task_exists(task_name):
                messages.add_message(request, messages.ERROR,'Task do not exists')
                return redirect('homepage')
        else:
            messages.add_message(request, messages.ERROR,'No task name provided')
            return redirect('homepage')
        count_todos = todo.check_len_db()
        if count_todos:
            try:
                todo.remove_task(task_name, request.user.id)
                messages.success(request,messages.SUCCESS ,f'Task {task_name} removed successfully')
                return redirect('homepage')
            except Exception as e:
                messages.success(request, messages.SUCCESS,f'Failed to remove a task: {str(e)}')
                return redirect('homepage')
    return render(request, 'homepage.html')

def finish_task(request, id):
    todo = TodoManager()
    try:
        todo.finish_task(id, request.user.id)
        messages.success(request, messages.SUCCESS,"Task finish with success.")
    except Exception as e:
        messages.error(request, f"Erro finish task: {str(e)}")

    return redirect('todopainel')

def sorted_view(request):
    todo = TodoManager()
    direction = request.POST.get('direction', 'ascending') # Default is ascending
    if direction == 'ascending':
        tasks_list = todo.order_by_asc_dsc(direction)
    elif direction == 'descending':
        tasks_list = todo.order_by_asc_dsc(direction)
    else:
        tasks_list = todo.tasks_list()
    context = {'tasks_list':tasks_list}
    return render(request, 'todopainel.html', context)

def category_filter(request):
    todo = TodoManager()
    category = request.POST.get('category')
    results = todo.filter_by_category(category)
    context = {'results':results}
    return render(request, 'todopainel.html', context)

def order_by_date(request):
    todo = TodoManager()
    created_date = request.POST.get('created_date')
    results = todo.order_by_date(created_date)
    context = {'results':results}
    return render(request, 'todopainel.html', context)

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
                    messages.add_message(request,messages.SUCCESS,f'Login successfull {user.username}')
                    login(request, user)
                    return redirect('homepage')
                else:
                    messages.add_message(request,messages.ERROR,f'User or password invalid')
                    return redirect('signin')
            except ValidationError as e:
                messages.add_message(request,messages.ERROR, e.message)
                return redirect('signin')
            
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            cpf = form.cleaned_data['cpf']
            password = form.cleaned_data['password']

            # Verify if user already exists
            if User.objects.filter(username=email).exists():
                messages.add_messages(request,messages.ERROR, f'{email} already exists')
                return redirect('signup')
            else:
                # Creating user and todo_user
                user = User.objects.create_user(username=email, password=password)
                todo_user = UserProfile.objects.create(user=user, name=name, email=email, cpf=cpf) # Associating user
                user.save()
                todo_user.save()

                user = authenticate(username=email, password=password)
                login(request, user)
                messages.add_message(request, messages.SUCCESS,f'User {user.username} created with success, Welcome!')
                return redirect('homepage')
    else:
        form = SignUpForm()  # If FORM is not POST

    return render(request, 'signup.html', {'form': form})

@login_required
def logout(request):
    user = request.user
    logout(user)
    return redirect('homepage')