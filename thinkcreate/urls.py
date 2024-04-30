from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from pages.views import page, index
from messaging.views import message
from .views import handler404
import os
from django.contrib import admin
from django.contrib.admin.sites import AdminSite 


admin.autodiscover()


admin.site_title = "SDSD"
    
urlpatterns = [

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('', index, name='index'),
    path('blog/', include('blog.urls')),
	path('account/', include('accounts.urls')),
    path('<slug>/', page, name='page'),
    path('contact/<username>', message, name='message'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'thinkcreate.views.handler404'