from django.forms import ModelForm
from .models import Comments
from django import forms


class CommentForm(ModelForm):
    '''Comment Form'''

    class Meta:
        model = Comments
        fields = ['body']

    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your message',
                'name': 'message',
                'rows': '6'
            }
        )
    )


class ContactForm(forms.Form):
    """ContactForm"""
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mr-0 ml-auto',
                'placeholder': 'Mike',
            }
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mr-0 ml-auto',
                'placeholder': 'mymailismike@email.com',
            }
        )
    )
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mr-0 ml-auto',
                'placeholder': 'Subject',
            }
        )
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control mr-0 ml-auto',
                'placeholder': 'Subject',
                'rows': 8,
            }
        )
    )
