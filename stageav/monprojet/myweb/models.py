from django.db import models
from django.forms import PasswordInput
from django.core.validators import MaxValueValidator
# Create your models here.
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class userManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse e-mail est obligatoire.")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **extra_fields)

class user(AbstractBaseUser):
    nom = models.CharField(max_length=70)
    prenom = models.CharField(max_length=70)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(validators=[MaxValueValidator(50)])
    nature = models.CharField(max_length=70)
    date = models.DateField()
    duree = models.IntegerField()
    etablissement = models.CharField(max_length=70)
    encadrant = models.ForeignKey('Encadrant', on_delete=models.SET_NULL, null=True, blank=True, related_name='stagiaires_encadres')
    sujet = models.ForeignKey('Sujet', on_delete=models.SET_NULL, null=True, blank=True, related_name='sujets_associes')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'age','nature','date','duree','etablissement','encadrant','sujet']


    objects = userManager()

    def __str__(self):
        return f"{self.nom} {self.prenom}"


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class EncadrantManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email est obligatoire.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Encadrant(AbstractBaseUser):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15)
    departement = models.CharField(max_length=100)
    nb_stagiaires_supervises = models.PositiveIntegerField(default=0)  # Champ pour le nombre de stagiaires supervisés
    sujet = models.ForeignKey('Sujet', on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'telephone', 'departement']

    objects = EncadrantManager()

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Sujet(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    stagiaire = models.OneToOneField(user, on_delete=models.SET_NULL, null=True, blank=True, related_name='sujet_associé')

    def __str__(self):
        return self.titre



class Identifier(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)


from django.db import models

class Score(models.Model):
    stagiaire = models.ForeignKey('user', on_delete=models.CASCADE)
    score = models.DecimalField(decimal_places=2, max_digits=5)
    def __str__(self):
        return f"Score de {self.stagiaire.nom} {self.stagiaire.prenom}: {self.score}"

from django.db import models



from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class RHManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email est obligatoire.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class RH(AbstractBaseUser):
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    departement = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'departement', 'telephone']

    objects = RHManager()
    def has_module_perms(self, app_label):
        return True
    def __str__(self):
        return self.email

 
class Tache(models.Model):
    fichier_pdf = models.FileField(upload_to='uploads/', blank=True, null=True)
    sujet = models.ForeignKey(Sujet, on_delete=models.CASCADE, related_name='taches')
    titre = models.CharField(max_length=100)
    date_debut = models.DateField()
    date_fin = models.DateField()
    description = models.TextField()
    def __str__(self):
        return self.titre

