from django.shortcuts import render
from .forms import MessageForm, ContactForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from accounts.views import profile
from accounts.models import User

# Create your views here.

def message(request, username):
	receiver = User.objects.all().filter(username=username)
	receiver = receiver.first()
	form = MessageForm(request=request, receiver=receiver)
	print(receiver)
	if request.method == 'POST':
		form = MessageForm(request=request, data=request.POST, receiver=receiver)
		if form.is_valid():
			form.save(commit=False)
			form.name = request.POST.get('name')
			form.email = request.POST.get('email')
			form.subject = request.POST.get('subject')
			form.message = request.POST.get('message')
			form.sender = request.user
			form.receiver = receiver
			form.save()
			messages.success(request, 'Message sent successfully.')
			return HttpResponseRedirect(request.path)

		else:
			form = MessageForm(request=request, receiver=receiver)
			messages.error(request, 'Failed to send the message.')
			print(form.errors)

	context = {

		'username': username,
		'form': form,
		'receiver': receiver
	}

	return render(request, 'contact.html', context)

def contact(request):
	flag = False;
	contact_form = ContactForm(request=request)
	if request.method == 'POST':
		contact_form = ContactForm(request=request, data=request.POST)
		if contact_form.is_valid():
			contact_form.save(commit=False)
			contact_form.name = request.POST.get('name')
			contact_form.email = request.POST.get('email')
			contact_form.subject = request.POST.get('subject')
			contact_form.message = request.POST.get('message')
			contact_form.sender = request.POST.get('sender')
			contact_form.save()
			messages.success(request, 'Message sent successfully.')
			return HttpResponseRedirect(request.path)
		else:
			contact_form = ContactForm(request=request)
			messages.error(request, 'Failed to send the message.')

	context = {
		'contact_form': contact_form,
	}
	# return {'contact_form': contact_form, 'flag': flag}
	return render(request, 'partials/_contact.html', context)