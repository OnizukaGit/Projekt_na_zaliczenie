from audioop import reverse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, CreateView
from django.contrib.auth import login, get_user_model, authenticate
from physiotherapist.forms import Loginform, Registerform
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect
from physiotherapist.models import GameScore
from django.db.models import Max
from django.db import models


User = get_user_model()


class StartPage(View):
    def get(self, request):
        ranking_data = (GameScore.objects.values('user__username')
                        .annotate(best_score=Max('score')).order_by('-best_score'))

        context = {
            'top_scores': ranking_data,
        }

        return render(request, 'basic.html', context)

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
        return response

class Game(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'game.html')

@method_decorator(csrf_exempt, name='dispatch')
class SaveScoreAPIView(LoginRequiredMixin, View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        score_value = request.POST.get('score')
        new_score = int(score_value)

        user = request.user

        best_score_so_far = GameScore.objects.filter(user=user).aggregate(models.Max('score'))['score__max']
        if best_score_so_far is None:
            best_score_so_far = -1

        if new_score > best_score_so_far:
            GameScore.objects.create(
                user=user,
                score=new_score
            )
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('home'))