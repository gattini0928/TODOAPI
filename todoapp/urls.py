from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('addtask/', add_task, name='add_task'),
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('todopainel/', todopainel, name='todopainel'),

]