from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
User = get_user_model()

class RegistrationForm(UserCreationForm):
    # username, password1, password2 уже есть в родителе
    email = forms.EmailField(label='Почта', required=True)

    class Meta:
        model = User
        fields = ['username', 'email'] #password1 + password2 писать не нужно

