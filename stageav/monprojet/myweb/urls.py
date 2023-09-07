from django.urls import path
from . import views
from  django.contrib.auth import views  as auth_views 


from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[

path('', views.login_view, name='login'),

path('logout/', views.logout_view, name='logout'),
  
  path('acc/', views.accview, name='accview'),
  path('add_encadrant/', views.add_encadrant, name='add_encadrant'),
  path('encadrants/', views.encadrant_view, name='encadrants'),
 path('update_encadrant/<int:id>/', views.update_encadrant, name='update_encadrant'),
 path('delete_encadrant/<int:id>/', views.delete_encadrant, name="delete_encadrant"),
 path('stagaire/', views.stagiaire_view, name='stagaireview'),  
 path('affectation/', views.affectation_view, name='affectation_view'),

  path('delete/<int:id>/', views.delete_data, name="deletedata"),
  path('<int:id>/', views.update_data, name="updatedata"),
  path('search_and_edit', views.search_and_edit, name='search_and_edit'),  # Vue de recherche et modification
   path('ajouter-sujet-interface/', views.ajouter_sujet_interface, name='ajouter_sujet_interface'),
  path('ajouter-sujet/<int:encadrant_id>/<int:stagiaire_id>/', views.ajouter_sujet, name='ajouter_sujet'),
    # URL pattern pour la vue de réussite de modification
  path('validation/<int:encadrant_id>/<int:stagiaire_id>/', views.valider_stagiaire, name='valider_stagiaire'),
  path('evaluer_encadrants_stagiaires/', views.evaluer_encadrants_stagiaires, name='evaluer_encadrants_stagiaires'), 
  path('afficher_score/<int:encadrant_id>/<int:stagiaire_id>/', views.afficher_score, name='afficher_score'),

  path('ajouter-rh/',views.ajouter_rh, name='ajouter_rh'),
  path('liste-rh/', views.liste_rh, name='liste_rh'),
  path('delete_rh/<int:id>/', views.delete_rh, name="delete_rh"),

path('rh/<int:id>/modifier/', views.update_rh, name='update_rh'),



  path('ajouter-sujet/', views.ajouter_sujet, name='ajouter_sujet'),
  path('ajouter-tache/<int:sujet_id>/', views.ajouter_tache, name='ajouter_tache'),
  path('liste-sujets/', views.liste_sujets, name='liste_sujets'),
   path('sujet/<int:sujet_id>/taches/', views.liste_taches, name='liste_taches'),
   path('soumettre-travail/<int:tache_id>/', views.soumettre_travail, name='soumettre_travail'),






path('edit_success/', views.edit_success, name='edit_success'),
 
  path('add_show', views.add_show, name='add_show'),]
# Ajoutez les chemins d'accès statiques pour les fichiers médias
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
