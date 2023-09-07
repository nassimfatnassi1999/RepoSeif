from django.contrib import admin
from .models import user ,Encadrant,Sujet,Score ,RH
# Register your models here.

@admin.register(user)
class useradmin(admin.ModelAdmin):
    list_display =('id','nom','prenom','email','age','nature','date','duree','etablissement')
  


@admin.register(Encadrant)
class EncadrantAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'prenom', 'email', 'telephone', 'departement']



@admin.register(Sujet)
class Sujetadmin(admin.ModelAdmin):
    list_display =('id','titre', 'description')


@admin.register(Score)
class Scoretadmin(admin.ModelAdmin):
    list_display =('id','stagiaire','score')



class RHadmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'email', 'departement', 'telephone', 'display_mot_de_passe_rh']

    def display_mot_de_passe_rh(self, obj):
        return obj.password

admin.site.register(RH, RHadmin)