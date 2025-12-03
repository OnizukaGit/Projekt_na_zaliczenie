from django.shortcuts import render
from django.template.context_processors import request
from django.views.generic import TemplateView, View


class StartPage(View):
    def get(self, request):
        return render(request, 'basic.html')

class Login(View):
    def get(self, request):
        return render(request, 'login.html')

class Register(View):
    def get(self, request):
        return render(request, 'register.html')
