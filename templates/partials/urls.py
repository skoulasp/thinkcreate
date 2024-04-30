
#Django pages app urls.py
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('/', views.page, name='home'),
]