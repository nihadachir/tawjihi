from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('etudiant/', etudiant_login, name='etudiant_login'),
    path('professeur/', professeur_login, name='professeur_login'),
    path('niveaux/<int:prof_id>/', afficher_niveaux, name='afficher_niveaux'),
    path('prof/<int:prof_id>/niveaux_classes/<int:niveau_id>/', afficher_classe, name='afficher_classe'),
    path('professeur/afficher_note/<int:prof_id>/<int:classe_id>/', afficher_note, name='afficher_note'),
    path('professeur/afficher_note/ajouter_note/<int:prof_id>/<int:classe_id>/', ajouter_note, name='ajouter_note'),
    path('note/modifier/<int:note_id>/<int:prof_id>/<int:classe_id>/', modifier_note, name='modifier_note'),
    path('supprimer_note/<int:note_id>/<int:prof_id>/<int:classe_id>/', supprimer_note, name='supprimer_note'),
    path('profile_prof/<int:prof_id>/',profile_prof, name='profile_prof'),
    path('log_out/', logout_view, name='logout_view'),
    path('historique_etudiant/<str:etudiant_id>/', historique_etudiant, name='historique_etudiant'),
    path('profile_etud/<str:etudiant_id>/', profile_etud, name='profile_etud'),
     path('etudiant/<str:etudiant_cne>/choices/', student_choices, name='student_choices'),
    path('etudiant/<str:etudiant_cne>/add_choice/', add_choice, name='add_choice'),
    path('modify_choice/<str:etudiant_cne>/<int:choice_id>/', modify_choice, name='modify_choice'),
    path('delete_choice/<str:etudiant_cne>/<int:choice_id>/', delete_choice, name='delete_choice'),
    path('afficher_resultat/<int:etd_id>/<str:etd_cne>/', afficher_resultat, name='afficher_resultat'),
    path('resultat/<int:etd_id>/<int:semestre>/', resultat, name='resultat'),

]
