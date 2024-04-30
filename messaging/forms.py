from django import forms
from .models import Message, ContactFormSubmissions

class MessageForm(forms.ModelForm):
	subject = forms.CharField(required=True)
	message = forms.CharField(widget=forms.Textarea(
                       attrs={'rows': 10,
                              'cols': 70}), required=True)

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop("request")
		receiver = kwargs.pop("receiver")
		super(MessageForm, self).__init__(*args, **kwargs)
		if self.request.user.is_authenticated:
			self.fields['sender'].initial = self.request.user
			self.fields['sender'].widget.attrs['hidden'] = True
			self.fields['receiver'].initial = receiver
			self.fields['receiver'].widget.attrs['hidden'] = True 

	class Meta:
		model = Message
		fields = ('sender', 'receiver', 'subject', 'message')


class ContactForm(forms.ModelForm):
	full_name = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	subject = forms.CharField(required=True)
	message = forms.CharField(widget=forms.Textarea(
                       attrs={'rows': 10,
                              'cols': 70}), required=True)
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop("request")
		super(ContactForm, self).__init__(*args, **kwargs)
		if self.request.user.is_authenticated:
			self.fields['sender'].initial = self.request.user
			self.fields['sender'].widget.attrs['hidden'] = True
			self.fields['full_name'].initial = self.request.user.full_name
			self.fields['full_name'].widget.attrs['hidden'] = True
			self.fields['email'].initial = self.request.user.email
			self.fields['email'].widget.attrs['hidden'] = True
		else:
			self.fields['sender'].widget.attrs['hidden'] = True
			self.fields['sender'].label = ''

	class Meta:
		model = ContactFormSubmissions
		fields = ('sender', 'full_name', 'email', 'subject', 'message')
    	
