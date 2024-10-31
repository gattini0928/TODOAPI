from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    cpf = models.CharField(max_length=15, null=True, blank=True)
    name = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(max_length=250, null=False, blank=False)

    def __str__(self):
        return f'UserProfile for {self.user.username}'

    