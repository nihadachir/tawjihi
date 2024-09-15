from django.contrib import admin
from .models import *
admin.site.register(Etudiant)
admin.site.register(Prof)
admin.site.register(Matiere)
admin.site.register(Note)
admin.site.register(Classe)
admin.site.register(Niveau)
admin.site.register(Choice)