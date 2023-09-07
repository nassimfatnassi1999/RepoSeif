from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from .models import RH, Encadrant, user

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, encadrant=False, stagiaire=False):
        try:
            if encadrant:
                user_model = Encadrant
            elif stagiaire:
                user_model = user
            else:
                user_model = RH  # Utilisez le modèle RH par défaut, vous pouvez ajouter de la logique pour gérer d'autres modèles ici

            user = user_model.objects.get(email=username)
            if user.check_password(password):
                return user
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None
