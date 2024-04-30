from pages.models import Page
from settings.models import SiteConfiguration, FooterConfiguration
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from messaging.forms import ContactForm
from django.contrib import messages
from django.urls import resolve
from django.template.loader import render_to_string, get_template

def page_display(request):
	pages = Page.objects.all().filter(is_published=True)
	settings = SiteConfiguration.objects.first()
	footer = FooterConfiguration.objects.first()
	return {'pages': pages, 'settings': settings, 'footer': footer}

def user_display(request):
	user = request.user
	return {'user': user}

def contact(request):
	template = render_to_string('partials/_contact.html')
	flag = False;
	contact_form = ContactForm(request=request)
	path = request.path
	match = resolve(path)
	if match.url_name == 'page':
		if request.method == 'POST':
			contact_form = ContactForm(request=request, data=request.POST)
			if contact_form.is_valid():
				contact_form.save(commit=False)
				contact_form.name = request.POST.get('name')
				contact_form.email = request.POST.get('email')
				contact_form.subject = request.POST.get('subject')
				contact_form.message = request.POST.get('message')
				contact_form.sender = request.user
				contact_form.save()
				messages.success(request, 'Message sent successfully.')
				contact_form = ContactForm(request=request)
			else:
				messages.error(request, 'Failed to send the message.')
				msg = 'Errors: %s' % contact_form.errors.as_text()
				print(msg)
			context = {
				'contact_form': contact_form,
				'template': template,
			}
	return {'contact_form': contact_form, 'flag': flag , 'template': template}