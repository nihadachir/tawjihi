from django.db import models

class Etudiant(models.Model):
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    cne = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=100)
    nom_tuteur = models.CharField(max_length=100)
    telephone = models.CharField(max_length=10)
    date_naissance = models.DateField()
    fk_classe = models.ForeignKey('app_tawjihi.Classe', on_delete=models.CASCADE)

    # Ajouter la nouvelle colonne 'id' avec primary_key=True
 
    
class Niveau(models.Model):
    nom = models.CharField(max_length=100)

class Note(models.Model):
    fk_etudiant = models.ForeignKey('Etudiant', on_delete=models.CASCADE)
    fk_prof = models.ForeignKey('Prof', on_delete=models.CASCADE)
    fk_matiere = models.ForeignKey('Matiere', on_delete=models.CASCADE)
    note = models.FloatField()
    semestre = models.IntegerField()

class Matiere(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    

class Prof(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    mail = models.EmailField()
    password = models.CharField(max_length=100)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

class Classe(models.Model):
    nom=models.CharField(max_length=100)
    nombre_etudiant = models.IntegerField()
    annee_scolaire = models.CharField(max_length=10)
    fk_niveau = models.ForeignKey('Niveau', on_delete=models.CASCADE)
    professeur = models.ForeignKey(Prof, on_delete=models.CASCADE)
    matieres = models.ManyToManyField('Matiere', related_name='classes')
    
    
class Choice(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    continue_in_school = models.BooleanField(default=True)
    reason_for_choice = models.TextField(blank=True, null=True)
    dream_job = models.TextField(blank=True, null=True)    