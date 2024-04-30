from django import forms
from .models import Post, Comment

class CommentForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your name',
        'name': 'name'
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'name': 'email'
    }))

    body = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'comment-textarea',
        'placeholder': 'Type your comment...',
        'id': 'usercomment',
        'rows': '10'
    }))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(CommentForm, self).__init__(*args, **kwargs)
        if self.request.user.is_authenticated:
            self.fields['name'].initial = self.request.user.full_name
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['email'].initial = self.request.user.email
            self.fields['email'].widget.attrs['readonly'] = True    


    class Meta:
        model = Comment
        fields = ('name', 'email', 'body', )



