from django.db import models
from accounts.models import User
from datetime import datetime

# Create your models here.
class Message(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
	subject = models.CharField(max_length=100)
	message = models.TextField()
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.subject


class ContactFormSubmissions(models.Model):
	sender = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='msg_sender')
	full_name = models.CharField(verbose_name="full name", max_length=60, null=True, blank=True)
	email = models.EmailField(verbose_name="email", max_length=60)
	subject = models.CharField(max_length=100)
	message = models.TextField()
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = "Contact form submissions"

	def __str__(self):
		return self.subject