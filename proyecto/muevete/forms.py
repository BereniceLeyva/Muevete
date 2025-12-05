from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email",
                             widget=forms.EmailInput(attrs={
                                 "placeholder": "Tu email",
                                 "id": "email"
                             }))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # placeholders y atributos para mantener el estilo de tu HTML
        self.fields['username'].widget.attrs.update({
            "placeholder": "Tu nombre de usuario",
            "id": "username"
        })
        self.fields['password1'].widget.attrs.update({
            "placeholder": "Tu contraseña",
            "id": "password"
        })
        
