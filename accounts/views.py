from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib import messages, auth
from .models import User
from .forms import UserUpdateForm, ProfileUpdateForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from blog.models import Post, Comment
from messaging.models import Message, ContactFormSubmissions
from accounts.forms import RegistrationForm, UserAuthenticationForm, UserUpdateForm
from blog.models import Post


def registration_view(request):
	context = {}
	user = request.user
	if user:
		if user.is_authenticated and user.is_admin != True:
			return redirect("dashboard")
		elif user.is_authenticated and user.is_admin == True:
			return HttpResponseRedirect(reverse('admin:index'))
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			username = form.cleaned_data.get('username')
			full_name = form.cleaned_data.get('full_name')
			raw_password = form.cleaned_data.get('password1')
			users = authenticate(email=email, password=raw_password)
			return redirect('login')
			messages.success(request, '- You are now registered and can log in')
		else:
			context['registration_form'] = form
			messages.error(request, 'Error:')

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'users/register.html', context)


def logout_view(request):
	logout(request)
	return redirect('/')

def login_view(request):
	context = {}
	form = UserAuthenticationForm(request.POST)
	if request.user:
		user = request.user
		if user.is_authenticated and user.is_admin != True:
			return redirect("blog")
		elif user.is_authenticated and user.is_admin == True:
			return HttpResponseRedirect(reverse('admin:index'))
	if request.POST:
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)
			if user:
				if user.is_authenticated and not (user.is_admin or user.is_staff) == True:
					login(request, user)
					return redirect("dashboard")
				elif user.is_authenticated and (user.is_admin or user.is_staff) == True:
					login(request, user)
					return HttpResponseRedirect(reverse('admin:index'))
		else:
			messages.error(request, 'Error: Wrong credentials.')
			context['login_form'] = form
	context['login_form'] = form
	return render(request, "users/login.html", context)

@login_required(login_url="/account/login/")
def users_view(request):
	context = {}
	all_likes = 0
	if not request.user.is_authenticated:
		return redirect("login")
	user = request.user
	usr_comments = Comment.objects.filter(user=user).order_by('-date')[:15]
	all_comments = Comment.objects.filter(user=user).all()
	for comment in all_comments:
		if (comment.get_total_likes()):
			all_likes = all_likes + comment.get_total_likes()
	comments = Comment.objects.all()
	posts = Post.objects.all().filter(is_published=True)
	messages_received = Message.objects.filter(receiver=user)
	messages_sent = Message.objects.filter(sender=user)
	contactform_submissions = ContactFormSubmissions.objects.filter(sender=user)
	context['user'] = user
	context['usr_comments'] = usr_comments
	context['comments'] = comments
	context['likes'] = all_likes
	context['posts'] = posts
	context['messages_received'] = messages_received
	context['contactform_submissions'] = contactform_submissions

	if request.POST:
		form = UserUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.initial = {
					"email": request.POST['email'],
					"username": request.POST['username'],
			}
			form.save()
			context['success_message'] = "Updated"
	else:
		form = UserUpdateForm(

			initial={
					"email": request.user.email, 
					"username": request.user.username,
				}
			)

	context['users_form'] = form

	return render(request, "users/dashboard.html", context)


def profile(request, username):
	profile = User.objects.filter(username=username).first()
	comments = Comment.objects.filter(user=profile)
	data = { 'profile': profile, 'comments': comments, 'username': username}
	return render(request, 'users/profile.html', data)

@login_required(login_url="/account/login/")
def edit_profile(request, username):
	data = {}
	usr_form = UserUpdateForm(instance=request.user)
	profile_form = ProfileUpdateForm(instance=request.user.profile)
	if request.POST:
		usr_form = UserUpdateForm(request.POST, instance=request.user)
		profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if usr_form.is_valid() and profile_form.is_valid():
			usr_form.save()
			profile_form.save()
			messages.success(request, 'Profile updated successfully.')
			return redirect('profile', username=request.POST['username'])
		else:
			message = messages.error(request, 'Error updating profile.')

	else:
		usr_form = UserUpdateForm(instance=request.user)
		profile_form = ProfileUpdateForm(instance=request.user.profile)
	profile = User.objects.filter(username=username).first()
	comments = Comment.objects.filter(user=profile)
	data = { 'profile': profile, 'comments': comments, 'username': username, 'usr_form': usr_form, 'profile_form': profile_form}
	return render(request, 'users/edit_profile.html', data)


@login_required(login_url="/account/login/")
def msg(request, username):
	context = {}
	if not request.user.is_authenticated:
		return redirect("login")
	user = request.user

	messages_received = Message.objects.filter(receiver=user)
	messages_sent = Message.objects.filter(sender=user)
	contactform_submissions = ContactFormSubmissions.objects.filter(sender=user)
	context['user'] = user
	context['messages_received'] = messages_received
	context['messages_sent'] = messages_sent
	context['contactform_submissions'] = contactform_submissions


	return render(request, "users/messages.html", context)



@login_required(login_url="/account/login/")
def msg_detail(request, username, id):
	context = {}
	message = Message.objects.filter(id=id).first()
	context['message'] = message
	if request.user.is_authenticated and (message.sender or message.receiver is request.user):
		
		return render(request, "users/message.html", context)
	else:
		return redirect("index")


