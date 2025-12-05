from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView, CreateView
from django.contrib.auth import login, logout, get_user_model, authenticate
from physiotherapist.forms import Loginform, Registerform
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
from physiotherapist.models import GameScore
from django.db.models import Max
from django.db import models

User = get_user_model()


class StartPage(View):
    def get(self, request):
        ranking_data = GameScore.objects.values('user__username').annotate(best_score=Max('score'))

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
        print(self.object)
        return response

class Game(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'game.html')


@method_decorator(csrf_exempt, name='dispatch')
class SaveScoreAPIView(LoginRequiredMixin, View):
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Wymagane logowanie'}, status=401)

        score_value = request.POST.get('score')

        try:
            new_score = int(score_value)
            user = request.user

            # 1. Znajdź najlepszy dotychczasowy wynik użytkownika
            # Używamy .aggregate() i Max do znalezienia najwyższego score
            best_score_so_far = GameScore.objects.filter(user=user).aggregate(models.Max('score'))['score__max']

            # Jeśli to jest pierwszy wynik, best_score_so_far będzie None
            if best_score_so_far is None:
                best_score_so_far = -1  # Ustawiamy na -1, aby każdy pierwszy wynik był lepszy

            # 2. Porównanie i zapis tylko lepszego wyniku
            if new_score > best_score_so_far:
                # Zapis nowego rekordu tylko, jeśli jest lepszy
                GameScore.objects.create(
                    user=user,
                    score=new_score
                )
                return redirect('home')
            else:
                # POPRAWIONA SKŁADNIA: Zwraca poprawnie sformatowany słownik JSON
                return JsonResponse({'status': 'info',
                                     'message': f'Wynik {new_score} jest niższy niż najlepszy ({best_score_so_far}).',
                                     'new_best': False})

                # UWAGA: Usuń atrybut 'data=' jeśli go użyłeś
                # Zrób też porządek z liniami w bloku 'except':


        except (ValueError, TypeError):  # Tutaj wyjątków się nie importuje

            return JsonResponse({'status': 'error', 'message': 'Nieprawidłowy format wyniku.'}, status=400)