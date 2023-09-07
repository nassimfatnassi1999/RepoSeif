from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import ObjectDoesNotExist
from .models import RH, Encadrant, user

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, encadrant=False, stagiaire=False, rh=False):
        user_model = None

        if encadrant:
            user_model = Encadrant
        elif stagiaire:
            user_model = user
        elif rh:
            user_model = RH

        if user_model:
            try:
                user_instance = user_model.objects.get(email=username)
                if user_instance.check_password(password):
                    return user_instance
            except ObjectDoesNotExist:
                return None
