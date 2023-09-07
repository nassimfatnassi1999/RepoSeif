from django.core import validators
from django import forms 
from .models import user,Encadrant
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

class StagiairRegistration(forms.ModelForm):
    encadrant = forms.ModelChoiceField(queryset=Encadrant.objects.all(), empty_label='Sélectionner un encadrant')
    class Meta:
        model = user 
        fields = ['nom','prenom','email','age','nature','date','duree','etablissement','encadrant']
        widgets = {
            'nom': forms.TextInput(attrs={'class':'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'age': forms.TextInput(attrs={'class':'form-control'}),
            'nature': forms.TextInput(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'class':'form-control'}),
            'duree': forms.TextInput(attrs={'class':'form-control'}),
            'etablissement': forms.TextInput(attrs={'class':'form-control'}),

        }
    def clean_encadrant(self):
        encadrant = self.cleaned_data['encadrant']

        # Vérifier si l'encadrant a atteint le maximum de stagiaires supervisés (5)
        if encadrant.nb_stagiaires_supervises >= 5:
            raise forms.ValidationError("Cet encadrant a déjà le maximum de stagiaires supervisés.")

        return encadrant

class StagiaireModificationForm(forms.ModelForm):
    class Meta:
        model = user
        fields = ['nom', 'prenom', 'email', 'age', 'nature', 'date', 'duree', 'etablissement']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'age': forms.TextInput(attrs={'class': 'form-control'}),
            'nature': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),  # Utilisation de DateInput
            'duree': forms.TextInput(attrs={'class': 'form-control'}),
            'etablissement': forms.TextInput(attrs={'class': 'form-control'}),
        }



class StagiaireSearchForm(forms.Form):
    stagiaire_id = forms.IntegerField(label='ID du Stagiaire')


from django.contrib.auth.forms import UserCreationForm














class EncadrantRegistration(forms.ModelForm):
    class Meta:
        model = Encadrant
        fields = ['nom', 'prenom', 'email', 'telephone', 'departement']
        widgets = {
            'nom': forms.TextInput(attrs={'class':'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class':'form-control'}),
            'departement': forms.TextInput(attrs={'class':'form-control'}),
        }


class StagiaireFilterForm(forms.Form):
    encadrant = forms.ModelChoiceField(queryset=Encadrant.objects.all(), empty_label='Tous les encadrants', required=False)





class EncadrantFilterForm(forms.Form):
    encadrant = forms.ModelChoiceField(queryset=Encadrant.objects.all(), empty_label='Tous les encadrants', required=False)
    def __init__(self, *args, **kwargs):
        super(EncadrantFilterForm, self).__init__(*args, **kwargs)
        self.fields['encadrant'].label_from_instance = lambda obj: obj.__str__()


from django import forms
from .models import Sujet

class SujetForm(forms.ModelForm):
    class Meta:
        model = Sujet
        fields = ['titre', 'description']  # Inclure uniquement les champs de titre et de description


from django import forms
from .models import RH

class RHForm(forms.ModelForm):
    class Meta:
        model = RH
        fields = ['nom', 'prenom', 'email', 'departement', 'telephone']
        widgets = { 
          

            }



from django import forms
from .models import Sujet, Tache

class TacheForm(forms.ModelForm):
    class Meta:
        model = Tache
        fields = ['titre', 'date_debut', 'date_fin', 'description']




from django import forms

class SoumissionTravailForm(forms.Form):
    fichier_pdf = forms.FileField(label='Fichier PDF')

from django.contrib.auth.forms import UserCreationForm

class AjoutRHForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    nom = forms.CharField(label='Nom')
    prenom = forms.CharField(label='Prénom')
    departement = forms.CharField(label='Département')
    telephone = forms.CharField(label='Téléphone')

    class Meta:
        model = RH
        fields = ('email', 'nom', 'prenom', 'departement', 'telephone')
from django.contrib.auth.forms import UserCreationForm
class AjouEncadrant(UserCreationForm):
    nom = forms.CharField(label='Nom')
    prenom = forms.CharField(label='Prénom')
    email = forms.EmailField(label='Email')
    departement = forms.CharField(label='Département')
    telephone = forms.CharField(label='Téléphone')
        
    class Meta:
        model = Encadrant
        fields = ('nom', 'prenom', 'email', 'departement','telephone')
        
class EncadrantLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    encadrant = forms.BooleanField(label='Je suis un Encadrant', required=False)
    stagiaire = forms.BooleanField(label='Je suis un stagiaire', required=False)


class LoginFormuser(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)


from django.contrib.auth.forms import UserCreationForm
class AjouuserForm(UserCreationForm):
    encadrant = forms.ModelChoiceField(queryset=Encadrant.objects.all(), empty_label='Sélectionner un encadrant')
    nom = forms.CharField(label='Nom')
    prenom = forms.CharField(label='Prénom')
    email = forms.EmailField(label='Email')
    age = forms.IntegerField(validators=[MaxValueValidator(50)])
    nature = forms.CharField(max_length=70)
    date = forms.DateField()
    duree = forms.IntegerField()
    etablissement = forms.CharField(max_length=70)
        
    class Meta:
        model = user
        fields = ('nom', 'prenom', 'email', 'age','nature','date','duree','etablissement','encadrant')
    def clean_encadrant(self):
        encadrant = self.cleaned_data['encadrant']

        # Vérifier si l'encadrant a atteint le maximum de stagiaires supervisés (5)
        if encadrant.nb_stagiaires_supervises >= 5:
            raise forms.ValidationError("Cet encadrant a déjà le maximum de stagiaires supervisés.")

        return encadrant