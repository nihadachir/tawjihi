from django import forms
from .models import Note, Etudiant, Matiere


class Notemod(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['note', 'semestre']
       