from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db.models import Q
from .models import Page
from settings.models import SiteConfiguration
from django.core.exceptions import ObjectDoesNotExist
import pprint
# Create your views here.

pp = pprint.PrettyPrinter(indent=4)

def index(request):
	obj = SiteConfiguration.objects.first()
	if obj is not None:
		get_homepage = obj.set_homepage
	else:
		get_homepage = False

	pp.pprint(get_homepage)
	context = {
		'homepage': get_homepage
	}
	return render(request, "pages/index.html", context)

def page(request, slug):
	page = get_object_or_404(Page, Q(is_published=True), slug=slug)
	print(page.page_link_location)
	context = {
		'page': page,
	}
	return render(request, "pages/page.html", context)


