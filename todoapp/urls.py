from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('todopainel/', todopainel, name='todopainel'),
    path('addtask/', add_task, name='add_task'),
    path('removetask/', remove_task, name='remove_task'),
    path('finishtask/<str:id>/', finish_task, name='finish_task'),

]