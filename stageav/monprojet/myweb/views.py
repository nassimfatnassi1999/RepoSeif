from django.shortcuts import render,redirect ,HttpResponseRedirect
from .forms import StagiairRegistration , EncadrantRegistration ,EncadrantFilterForm
from django.contrib import messages
from .forms import LoginForm
from .models import Identifier
from django.contrib.auth.decorators  import login_required
from .models import user,Encadrant
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
from .forms import AjouEncadrant , AjouuserForm
from .custom_auth_backend import CustomAuthBackend

# Create your views here.
def add_show(request):
    encadrant_filter_form = EncadrantFilterForm(request.GET)
    stagiaires = user.objects.all()

    # Filtrer les stagiaires en fonction de l'encadrant sélectionné dans le formulaire
    encadrant = request.GET.get('encadrant')
    if encadrant:
        stagiaires = stagiaires.filter(encadrant=encadrant)

    # Rechercher les stagiaires en fonction de la durée du stage saisie par l'utilisateur
    duree_stage = request.GET.get('duree_stage')
    if duree_stage:
        stagiaires = stagiaires.filter(duree__icontains=duree_stage)

    if request.method == 'POST':
        fm = AjouuserForm(request.POST)
        if fm.is_valid():
            stagiaire = fm.save()

            # Mettre à jour le nombre de stagiaires supervisés par l'encadrant
            encadrant = stagiaire.encadrant
            if encadrant is not None:
                encadrant.nb_stagiaires_supervises = stagiaires.filter(encadrant=encadrant).count()
                encadrant.save()

            return redirect('add_show')
    else:
        fm = AjouuserForm()

    return render(request, 'myweb/ajaff.html', {'form': fm, 'sta': stagiaires, 'encadrant_filter_form': encadrant_filter_form})


from django.shortcuts import render, get_object_or_404
from .forms import StagiaireSearchForm, StagiaireModificationForm


def search_and_edit(request):
    error_message = ''
    success_message = ''
    search_form = StagiaireSearchForm()
    modification_form = None

    if request.method == 'POST':
        search_form = StagiaireSearchForm(request.POST)
        if search_form.is_valid():
            stagiaire_id = search_form.cleaned_data['stagiaire_id']
            try:
                stagiaire = user.objects.get(pk=stagiaire_id)
            except user.DoesNotExist:
                stagiaire = None

            if stagiaire:
                if 'edit_mode' in request.POST:
                    modification_form = StagiaireModificationForm(request.POST, instance=stagiaire)
                    if modification_form.is_valid():
                        modification_form.save()  # Enregistrement des modifications dans la base de données
                        success_message = 'Modification enregistrée avec succès.'
                else:
                    modification_form = StagiaireModificationForm(instance=stagiaire)
            else:
                error_message = 'Aucun stagiaire trouvé avec cet ID.'

    context = {
        'search_form': search_form,
        'modification_form': modification_form,
        'error_message': error_message,
        'success_message': success_message,
    }

    return render(request, 'myweb/mod.html', context,{'form':fm})






def login_view(request):
    error_message = None

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            encadrant = form.cleaned_data.get('encadrant', False)
            stagiaire = form.cleaned_data.get('stagiaire', False)
            user = authenticate(request, username=email, password=password, encadrant=encadrant, stagiaire=stagiaire)
            if user is not None:
                login(request, user)
                return redirect('add_show')  # Redirigez vers la page appropriée après une connexion réussie
            else:
                error_message = "Nom d'utilisateur ou mot de passe incorrect."

    else:
        form = LoginForm()

    return render(request, 'myweb/login.html', {'form': form, 'error_message': error_message})

from django.shortcuts import render





from django.shortcuts import render

def edit_success(request):
    return render(request, 'myweb/edit_success.html')  # Assurez-vous que le chemin du template est correct

#suprimmer 
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

def delete_data(request, id):
    stagiaire = get_object_or_404(user, pk=id)
    encadrant = stagiaire.encadrant  # Récupérer l'encadrant supervisant le stagiaire

    # Mettre à jour le nombre de stagiaires supervisés par l'encadrant
    if encadrant.nb_stagiaires_supervises > 0:
        encadrant.nb_stagiaires_supervises -= 1
        encadrant.save()

    stagiaire.delete()
    return HttpResponseRedirect('/')


#modification
#def update_data(request, id):
    #if request.method == 'POST':  # Utilisez 'POST' en majuscules
       # pi = user.objects.get(pk=id)
      #  fm = StagiairRegistration(request.POST, instance=pi)  # Utilisez StagiaireModificationForm
     #   if fm.is_valid():
     #       fm.save()
    #else:
      #  pi = user.objects.get(pk=id)
     #   fm = StagiairRegistration(instance=pi)  # Utilisez StagiaireModificationForm
    #return render(request, 'myweb/mod.html', {'form': fm})
def update_data(request, id):
    pi = get_object_or_404(user, pk=id)  # Utilisation de get_object_or_404 pour obtenir l'objet ou 404 si non trouvé

    if request.method == 'POST':
        fm = StagiairRegistration(request.POST, instance=pi)

        if fm.is_valid():
            fm.save()
            messages.success(request, "Les données ont été modifiées avec succès.")  # Message de succès
            return redirect('add_show')  # Redirigez où vous voulez après la modification réussie
        else:
            messages.error(request, "La modification a échoué. Veuillez corriger les erreurs.")  # Message d'échec

    else:
        fm = StagiairRegistration(instance=pi)

    return render(request, 'myweb/mod.html', {'form': fm})


#def accview(request):
 #   if request.method == 'POST':
  #      fm = StagiairRegistration(request.POST)
   #     if fm.is_valid():
    #        fm.save()
    #else:
     #   fm = StagiairRegistration()
    
   # stag = user.objects.all()  # Récupérez tous les stagiaires enregistrés
    
    #return render(request, 'myweb/acc.html', {'form': fm, 'sta': stag})

def accview(request):
    if request.method == 'POST':
        fm = AjouuserForm(request.POST)
        if fm.is_valid():
            stagiaire = fm.save()

            # Mettre à jour le nombre de stagiaires supervisés par l'encadrant
            encadrant = stagiaire.encadrant
            if encadrant is not None:
                encadrant.nb_stagiaires_supervises += 1
                encadrant.save()

            return redirect('accview')
    else:
        fm = AjouuserForm()

    stag = user.objects.all()
    return render(request, 'myweb/acc.html', {'form': fm, 'sta': stag})


def encadrant_view(request):
    encadrants = Encadrant.objects.all()  # Récupérez tous les encadrants de la base de données
    return render(request, 'myweb/shen.html', {'encadrants': encadrants})



def add_encadrant(request):
    if request.method == 'POST':
        encadrant_form = AjouEncadrant(request.POST)
        if encadrant_form.is_valid():
            encadrant_form.save()
            return redirect('encadrants')  # Rediriger vers la liste des encadrants après l'ajout
    else:
        encadrant_form = AjouEncadrant()
    
    return render(request, 'myweb/add_encadrant.html', {'encadrant_form': encadrant_form})







def update_encadrant(request, id):
    encadrant = get_object_or_404(Encadrant, pk=id)
    if request.method == 'POST':
        encadrant_form = EncadrantRegistration(request.POST, instance=encadrant)
        if encadrant_form.is_valid():
            encadrant_form.save()
            return redirect('encadrants')  # Rediriger vers la liste des encadrants après la modification
    else:
        encadrant_form = EncadrantRegistration(instance=encadrant)
    
    return render(request, 'myweb/mod_en.html', {'encadrant_form': encadrant_form})



def delete_encadrant(request, id):
    if request.method == 'POST':
        try:
            # Essayer de récupérer l'objet Encadrant par son ID
            encadrant = Encadrant.objects.get(pk=id)
            encadrant.delete()
        except Encadrant.DoesNotExist:
            pass  # Si l'objet Encadrant n'existe pas, simplement ignorer
    return redirect('encadrants')  # Rediriger vers la liste des encadrants après la suppression






def stagiaire_view(request):
    stag = user.objects.all()  # Récupérez tous les encadrants de la base de données
    return render(request, 'myweb/ajaff.html',{'sta':stag})


def affectation_view(request):
    return render(request, 'myweb/affectation.html')



from django.shortcuts import render, redirect
from .models import Sujet, Tache
from .forms import SujetForm, TacheForm

from django.shortcuts import redirect

from django.shortcuts import reverse

def ajouter_sujet(request, encadrant_id, stagiaire_id):
    encadrant = Encadrant.objects.get(pk=encadrant_id)
    stagiaire = user.objects.get(pk=stagiaire_id)

    # Vérifier si un sujet existe déjà pour ce stagiaire
    if Sujet.objects.filter(stagiaire=stagiaire).exists():
        return redirect('ajouter_sujet_interface')

    if request.method == 'POST':
        form = SujetForm(request.POST)
        if form.is_valid():
            sujet = form.save(commit=False)
            sujet.encadrant = encadrant
            sujet.stagiaire = stagiaire
            sujet.save()
            
            sujet_id = sujet.id  # Récupérer l'ID du nouveau sujet
            
            # Vérifier si l'ID du sujet est valide avant de rediriger
            if sujet_id is not None:
                url = reverse('ajouter_tache', kwargs={'sujet_id': sujet_id})
                return redirect(url)
    else:
        form = SujetForm()

    context = {
        'form': form,
        'encadrant': encadrant,
        'stagiaire': stagiaire,
    }

    return render(request, 'myweb/ajouter_sujet.html', context)


def ajouter_tache(request, sujet_id):
    sujet = Sujet.objects.get(pk=sujet_id)

    if request.method == 'POST':
        form = TacheForm(request.POST)
        if form.is_valid():
            tache = form.save(commit=False)
            tache.sujet = sujet
            tache.save()
            return redirect('liste_taches', sujet_id=sujet_id)  # Utilisation de sujet.id au lieu de sujet_id
    else:
        form = TacheForm()

    return render(request, 'myweb/ajouter_tache.html', {'form': form, 'sujet': sujet})



def liste_sujets(request):
    sujets = Sujet.objects.all()
    return render(request, 'liste_sujets.html', {'sujets': sujets})

from django.shortcuts import render, get_object_or_404
from .models import Sujet

from django.utils import timezone
from datetime import datetime

from django.contrib import messages

def liste_taches(request, sujet_id):
    sujet = Sujet.objects.get(id=sujet_id)
    taches = Tache.objects.filter(sujet=sujet)
    
    maintenant = timezone.now()
    for tache in taches:
        date_fin = datetime.combine(tache.date_fin, datetime.min.time())
        date_fin_aware = timezone.make_aware(date_fin, timezone.get_current_timezone())

        if   date_fin_aware < maintenant:
            tache.est_expiree = True
            messages.warning(request, f"La tâche '{tache.titre}' est expirée.")
        else:
            tache.est_expiree = False
    
    return render(request, 'myweb/liste_taches.html', {'sujet': sujet, 'taches': taches})

from django.shortcuts import render
from .models import Encadrant, user
from .forms import SujetForm  # Assurez-vous d'importer le formulaire SujetForm

def ajouter_sujet_interface(request):
    encadrants = Encadrant.objects.all()
    stagiaires = user.objects.all()

    context = {
        'encadrants': encadrants,
        'stagiaires': stagiaires,
    }

    return render(request, 'myweb/affectation.html', context)


from django.shortcuts import render
from .models import Encadrant

def evaluer_encadrants_stagiaires(request):
    encadrants = Encadrant.objects.all()
    
    context = {
        'encadrants': encadrants,
    }
    
    return render(request, 'myweb/valider_stagiaire.html', context)



from django.shortcuts import render, get_object_or_404, redirect
from .models import Encadrant, user, Score

def valider_stagiaire(request, encadrant_id, stagiaire_id):
    encadrant = get_object_or_404(Encadrant, pk=encadrant_id)
    stagiaire = get_object_or_404(user, pk=stagiaire_id)

    criteres = ['Motivation personnelle de l’étudiant', 'Esprit d’initiative', 'Evolution remarquée dans l’apprentissage et le cheminement de l’étudiant',
    'Capacité d’assumer les responsabilités qui lui sont confiées','Capacité de travail en groupe','Facilité d’adaptation aux divers changements rencontrés dans son travail',
    'Capacité de communiquer par écrit','Capacité de s’exprimer en public','A la volonté de progresser',
    'Tient compte des remarques','S’intéresse aux activités proposées','Sait être attentif(ve)','Est capable de travailler seul','Réalise un travail avec soin et précision','Respecte les consignes']
    
    niveaux = [
        ('Excellent', 4),
        ('Très bon', 3),
        ('Satisfaisant', 2),
        ('Insatisfaisant', 1),
    ]
    poids_niveaux = {
        'Excellent': 4,
        'Très bon': 3,
        'Satisfaisant': 2,
        'Insatisfaisant': 1,
    }

    score_calculated = None  # Initialisation du score calculé
    error_message = None  # Initialisation du message d'erreur

    if request.method == 'POST':
        action = request.POST.get('action')  # Récupérer l'action soumise dans le formulaire
        if action == 'calculer_score':
            total_score = 0
            all_levels_chosen = True  # Variable pour vérifier si tous les niveaux ont été choisis
            for critere in criteres:
                niveau = request.POST.get(critere)
                if niveau:
                    total_score += poids_niveaux[niveau]
                else:
                    all_levels_chosen = False

            if all_levels_chosen:
                score_calculated = total_score

                # Enregistrez le score dans la table Score
                Score.objects.create(stagiaire=stagiaire, score=score_calculated)

                # Marquez le stagiaire comme validé en mettant à jour son champ "valide"
                stagiaire.valide = True
                stagiaire.save()

                # Rediriger vers la page valider_stagiaire avec l'ID de l'encadrant et du stagiaire
                return redirect('valider_stagiaire', encadrant_id=encadrant.id, stagiaire_id=stagiaire.id)
            else:
                error_message = "Veuillez choisir un niveau de performance pour chaque critère."

    else:
        # Récupérer le dernier score du stagiaire s'il en existe un
        try:
            dernier_score = Score.objects.filter(stagiaire=stagiaire).latest('id')
            score_calculated = dernier_score.score
        except Score.DoesNotExist:
            score_calculated = None

    context = {
        'encadrant': encadrant,
        'stagiaire': stagiaire,
        'criteres': criteres,
        'niveaux': niveaux,
        'score_calculated': score_calculated,
        'error_message': error_message,  # Ajout du message d'erreur dans le contexte
    }

    return render(request, 'myweb/validation.html', context)

from django.shortcuts import render, get_object_or_404
from .models import user, Score

def afficher_score(request, encadrant_id, stagiaire_id):
    stagiaire = get_object_or_404(user, pk=stagiaire_id)
    
    # Récupérer le score du stagiaire depuis la table Score
    scores = Score.objects.filter(stagiaire=stagiaire)
    
    context = {
        'stagiaire': stagiaire,
        'scores': scores,
    }
    
    return render(request, 'myweb/afficher_score.html', context)


from django.shortcuts import render, redirect
from .forms import RHForm



from django.shortcuts import render
from .models import RH

from django.shortcuts import render
from .models import RH
def liste_rh(request):
    search_term = request.GET.get('search')
    departement_id = request.GET.get('departement')

    rh_objects = RH.objects.all()

    if search_term:
        rh_objects = rh_objects.filter(nom__icontains=search_term)

    if departement_id:
        rh_objects = rh_objects.filter(departement_id=departement_id)

    context = {
        'rh_objects': rh_objects,
        'search_term': search_term,
        'departement_id': departement_id
    }

    return render(request, 'myweb/rh_list.html', context)

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import RH
def delete_rh(request, id):
    if request.method == 'POST':
        try:
            # Essayer de récupérer l'objet Encadrant par son ID
            rh = RH.objects.get(pk=id)
            rh.delete()
        except RH.DoesNotExist:
            pass  # Si l'objet Encadrant n'existe pas, simplement ignorer
    return redirect('liste_rh')  # Rediriger vers la liste des encadrants après la suppression


from django.shortcuts import render, get_object_or_404, redirect
from .models import RH
from .forms import RHForm

def update_rh(request, id):
    rh = get_object_or_404(RH, pk=id)
    if request.method == 'POST':
        rh_form = RHForm(request.POST, instance=rh)
        if rh_form.is_valid():
            rh_form.save()
            return redirect('liste_rh')  # Rediriger vers la liste des RH après la modification
    else:
        rh_form = RHForm(instance=rh)
    
    return render(request, 'myweb/mod_rh.html', {'rh_form': rh_form})




from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SoumissionTravailForm

from django.contrib import messages
from .forms import SoumissionTravailForm

def soumettre_travail(request, tache_id):
    # Récupérer la tâche correspondante à l'ID
    tache = Tache.objects.get(id=tache_id)

    if request.method == 'POST':
        form = SoumissionTravailForm(request.POST, request.FILES)
        if form.is_valid():
            # Enregistrer le fichier PDF soumis
            fichier_pdf = form.cleaned_data['fichier_pdf']
            tache.fichier_pdf = fichier_pdf
            tache.save()

            messages.success(request, "Le travail a été soumis avec succès !")
            return redirect('liste_taches', sujet_id=tache.sujet.id)  # Rediriger vers la liste des tâches avec l'ID du sujet

    else:
        form = SoumissionTravailForm()

    context = {
        'tache': tache,
        'form': form,
    }
    return render(request, 'myweb/soumettre_travail.html', context)


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import RHForm

def login_rh(request):
    error_message = None

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('encadrants')  # Rediriger vers le tableau de bord après la connexion réussie
            else:
                error_message = "Identifiants invalides. Veuillez réessayer."
    else:
        form = LoginForm()

    return render(request, 'myweb/encadrantlogin.html', {'form': form, 'error_message': error_message})


from django.shortcuts import render, redirect
from .forms import RHForm,AjoutRHForm

def ajouter_rh(request):
    if request.method == 'POST':
        form = AjoutRHForm(request.POST)
        if form.is_valid():
            rh = form.save()
            # Traitez les autres actions après l'ajout du membre RH
            return redirect('liste_rh')
    else:
        form = AjoutRHForm()
    return render(request, 'myweb/rhadd.html', {'form': form})


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import EncadrantLoginForm

def loginencadrant(request):
    if request.method == 'POST':
        form = EncadrantLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # Rediriger vers une page appropriée après la connexion réussie
                return redirect('add_show')
            else:
                # Gérer le cas d'authentification invalide
                form.add_error(None, "Les informations d'identification sont invalides.")
    else:
        form = EncadrantLoginForm()
    
    context = {
        'form': form,
    }
    return render(request, 'myweb/encadrantlogin.html', context)



from .forms import LoginFormuser
def userlogin(request):
    if request.method == 'POST':
        form = LoginFormuser(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # Rediriger vers une page appropriée après la connexion réussie
                return redirect('add_show')
            else:
                # Gérer le cas d'authentification invalide
                form.add_error(None, "Les informations d'identification sont invalides.")
    else:
        form = LoginFormuser()
    
    context = {
        'form': form,
    }
    return render(request, 'myweb/userlogin.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige vers la page de connexion
