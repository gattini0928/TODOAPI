from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")  # Relacionamento com User padrão
    cpf = models.CharField(max_length=15, null=True, blank=True)
    # Outros campos específicos do perfil do usuário
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=250)

    def __str__(self):
        return f'UserProfile for {self.user.username}'

    