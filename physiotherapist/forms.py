from cProfile import label

from django import forms
from django.core.validators import ValidationError
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class Loginform(forms.Form):
    username = forms.CharField(label="Nazwa użytkownika")
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)

    def clean(self):
        cd = super().clean()

        username = cd.get('username')
        password = cd.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            raise ValidationError("Złe podane hasło lub login")


class Registerform(forms.ModelForm):
    pass1 = forms.CharField(label="Hasło", widget=forms.PasswordInput)
    pass2 = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
        )
        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'username': 'Login',
            'email': 'Email',

        }
        help_texts = {
            'username': 'Tym będziesz się logował',
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Ta nazwa użytkownika już istnieje")
        return username

    def clean(self):
        cd = super().clean()
        pass1 = cd.get('pass1')
        pass2 = cd.get('pass2')
        if len(pass1) < 4:
            raise ValidationError('Hasło musi mieć więcej niż 4 litery!')
        if pass1 != pass2:
            raise ValidationError('Hasło musi być takie same')