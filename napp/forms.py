from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class createUser(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password1','password2']
        
        widgets={
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter First Name','class': 'user_name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter Last Name','class': 'user_name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter Username','class': 'user_name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Your Email Address','class': 'user_name'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'placeholder': '••••••••',
            'class': 'user_name'
        })

        self.fields['password2'].widget.attrs.update({
            'placeholder': '••••••••',
            'class': 'user_name'
        })