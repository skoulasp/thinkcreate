from django.contrib import admin
from .models import Message, ContactFormSubmissions

# Register your models here.

class MessageAdmin(admin.ModelAdmin):
	list_display = ('subject', 'message', 'sender', 'receiver', 'date')
	
	# list_filter = ('date', 'is_published')


class ContactFormSubmissionsAdmin(admin.ModelAdmin):
	list_display = ('subject', 'message', 'sender', 'email', 'full_name', 'date',)
	readonly_fields = ['date', 'sender', 'full_name', 'email', 'subject', 'message',]

	def get_readonly_fields(self, request, obj=None):
	    if obj:
	        return ['date', 'sender', 'full_name', 'email', 'subject', 'message',]
	    else:
	        return []

admin.site.register(Message, MessageAdmin)
admin.site.register(ContactFormSubmissions, ContactFormSubmissionsAdmin)