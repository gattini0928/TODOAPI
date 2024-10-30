from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .mongo_models import *
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime
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
                todo.add_task(task_name, category, priority, created_at, due_date, status)
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
                todo.remove_task(task_name)
                messages.success(request,f'Task {task_name} removed successfully')
                return redirect('homepage')
            except Exception as e:
                messages.error(request,f'Failed to remove a task: {str(e)}')
                return redirect('homepage')
    return render(request, 'homepage.html')

def finish_task(request, id):
    todo = TodoManager()
    try:
        todo.finish_task(id)
        messages.success(request, "Task finish with success.")
    except Exception as e:
        messages.error(request, f"Erro finish task: {str(e)}")

    return redirect('todopainel')


def todopainel(request):
    todo = TodoManager()
    tasks = todo.tasks_list()
    context = {'tasks':tasks}
    return render(request, 'todopainel.html', context)

def signin(request):
    return render(request, 'signin.html')

def signup(request):
    return render(request, 'signup.html')