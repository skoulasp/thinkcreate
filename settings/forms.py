from django import forms
from .models import *

class ChoiceForm(forms.Form):
    field = forms.ChoiceField(required=True, widget=forms.RadioSelect(
    attrs={'class': 'Radio'}), choices=(('light','Light'),('dark','Dark'),))