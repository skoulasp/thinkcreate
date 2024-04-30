from django.urls import path
from . import views

urlpatterns = [
	path('login/', views.login_view, name='login'),
	path('register/', views.registration_view, name='register'),
	path('logout/', views.logout_view, name='logout'),
	path('dashboard/', views.users_view, name='dashboard'),
	path('profile/<username>', views.profile, name='profile'),
	path('profile/<username>/edit', views.edit_profile, name='edit'),
	path('profile/<username>/messages', views.msg, name='msg'),
	path('profile/<username>/messages/<id>', views.msg_detail, name='msg_detail'),
]