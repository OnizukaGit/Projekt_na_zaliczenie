from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class GameScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    class Meta:
        ordering = ['-score',]

    def __str__(self):
        return f"Wynik {self.user.username}: {self.score}"