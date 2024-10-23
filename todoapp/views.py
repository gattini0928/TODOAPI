from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from todoapi.database.pymongo_config import get_db

def homepage(request):
    context = {'Hello':'hello'}
    return render(request, 'homepage.html', context)

