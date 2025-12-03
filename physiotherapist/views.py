from django.contrib.auth.views import LoginView, redirect_to_login, LogoutView
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, FormView, RedirectView, CreateView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, get_user_model, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from physiotherapist.forms import Loginform, Registerform


User = get_user_model()


class StartPage(View):
    def get(self, request):
        return render(request, 'basic.html')

class Login(FormView):
    template_name = 'login.html'
    success_url = reverse_lazy('home')
    form_class = Loginform

    def form_valid(self, form):
        password = form.cleaned_data['password']
        username = form.cleaned_data['username']
        user = authenticate(password=password, username=username)
        login(self.request, user)
        return super().form_valid(form)


class Logout(RedirectView):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(Logout, self).get(request, *args, **kwargs)


class Register(CreateView):
    model = User
    template_name = 'register.html'
    form_class = Registerform
    success_url = reverse_lazy('home')
    permission_required = 'auth.add_user'

    def form_valid(self, form):
        response = super().form_valid(form)
        cd = form.cleaned_data
        self.object.set_password(cd['pass1'])
        self.object.save()
        login(self.request, self.object)
        print(self.object)
        return response

class Game(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'game.html')