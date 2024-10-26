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
        print(data)
        if data:
            task_name = data.get('name')
            category = data.get('category')
            priority = float(data.get('priority', 0)) # Default Value 0
            created_at = datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
            due_date = data.get('due_date')
            status = data.get('status') or 'Pending'

            todo = TodoManager()
            try:
                todo.add_task(task_name, category, priority, created_at, due_date, status)
                messages.success(request, 'Task created successfully!')
                return redirect('homepage')
            except Exception as e:
                return messages.error('Failed to add a task' , str(e))

    return render(request,'homepage.html')

def todopainel(request):
    return render(request, 'todopainel.html')

def signin(request):
    return render(request, 'signin.html')

def signup(request):
    return render(request, 'signup.html')