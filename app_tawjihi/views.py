from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.db.models import Sum
from datetime import date

def home(request):
    return render(request, 'home.html')


def etudiant_login(request):
    if request.method == 'POST':
        cne = request.POST['cne']
        password = request.POST['password']
        try:
            etudiant = Etudiant.objects.filter(cne=cne).first()
            if etudiant:
                if etudiant.password == password:
                    # Authentification réussie
                    return redirect('historique_etudiant', etudiant_id=etudiant.cne)
                else:
                    # Mot de passe incorrect
                    messages.error(request, "Mot de passe incorrect.")
            else:
                # Étudiant non trouvé
                messages.error(request, "CNE incorrect.")
        except Etudiant.DoesNotExist:
            # Gérer l'exception si nécessaire
            messages.error(request, "Erreur lors de la recherche de l'étudiant.")
    return render(request, 'etudiant.html')



def professeur_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            professeur = Prof.objects.get(mail=email)
            if professeur.password == password:
                return redirect('afficher_niveaux', prof_id=professeur.id)
            else:
                messages.error(request, "Mot de passe incorrect.")
        except Prof.DoesNotExist:
            messages.error(request, "Email incorrect.")



def profile_prof(request,prof_id):
    professeur = Prof.objects.get(id=prof_id)
    matieres = Matiere.objects.filter(prof=professeur)
    classes = Classe.objects.filter(professeur=professeur)

    # Créer un dictionnaire vide pour stocker les classes par niveau
    classes_par_niveau = {}

    # Regrouper les classes par niveau
    for classe in classes:
        if classe.fk_niveau not in classes_par_niveau:
            classes_par_niveau[classe.fk_niveau] = [classe]
        else:
            classes_par_niveau[classe.fk_niveau].append(classe)

    context = {
        'prof': professeur,
        'matieres': matieres,
        'classes': classes,
        'classes_par_niveau': classes_par_niveau,
    }
    return render(request, 'profile_prof.html', context)


def profile_etud(request,etudiant_id):
    etudiant = Etudiant.objects.filter(cne=etudiant_id).first()
   
    return render(request, 'profile_etud.html', {'etudiant': etudiant})



def afficher_niveaux(request, prof_id):
    professeur = get_object_or_404(Prof, id=prof_id)
    classes = Classe.objects.filter(professeur=professeur)
    niveaux_ids = set(classe.fk_niveau_id for classe in classes)
    niveaux = Niveau.objects.filter(id__in=niveaux_ids).distinct()
    # Calculate total number of students
    total_students = Etudiant.objects.filter(fk_classe__in=classes).count()
    # Calculate total number of levels
    total_levels = niveaux.count()
    # Initialize a dictionary to store student counts per level
    students_per_level = {}
    # Calculate the number of students for each level taught by the professor
    for niveau in niveaux:
        # Get all classes for this level taught by the professor
        classes_niveau = classes.filter(fk_niveau=niveau)
        # Count students for these classes
        student_count = Etudiant.objects.filter(fk_classe__in=classes_niveau).count()
        students_per_level[niveau.nom] = student_count

    return render(request, 'niveaux.html', {'niveaux': niveaux, 'prof': professeur, 'total_students': total_students, 'total_levels': total_levels, 'students_per_level': students_per_level})


def afficher_classe(request, prof_id, niveau_id):
    professeur = get_object_or_404(Prof, id=prof_id)
    niveau = get_object_or_404(Niveau, id=niveau_id)
    classes = Classe.objects.filter(professeur=professeur, fk_niveau=niveau)
    return render(request, 'classes_par_niveau.html', {'classes': classes, 'niveau': niveau, 'prof': professeur})


# views.py
def afficher_note(request, prof_id, classe_id):
    professeur = get_object_or_404(Prof, id=prof_id)
    classe = get_object_or_404(Classe, id=classe_id)
    notes = Note.objects.filter(fk_prof=professeur, fk_etudiant__fk_classe=classe,fk_matiere=professeur.matiere)
    return render(request, 'professeur.html', {'notes': notes, 'prof': professeur, 'classe': classe})


# views.py
def ajouter_note(request, prof_id, classe_id):
    professeur = get_object_or_404(Prof, id=prof_id)
    classe = get_object_or_404(Classe, id=classe_id, professeur=professeur)  # Assurez-vous que la classe est enseignée par ce professeur

    # Obtenir les étudiants dans la classe enseignée par ce professeur
    etudiants = Etudiant.objects.filter(fk_classe=classe)

    # Le professeur enseigne la matière liée via le champ matiere dans le modèle Prof
    matiere = professeur.matiere

    if request.method == 'POST':
        etudiant_cne = request.POST.get('etudiant_cne')
        note_value = request.POST.get('note')
        semestre = request.POST.get('semestre')
        etudiant = Etudiant.objects.filter(cne=etudiant_cne).first()

        Note.objects.create(
            fk_etudiant=etudiant,
            fk_prof=professeur,
            fk_matiere=matiere,
            note=note_value,
            semestre=semestre
        )
        return redirect('afficher_note', prof_id=prof_id, classe_id=classe_id)
    else:
        return render(request, 'ajouter_note.html', {
            'etudiants': etudiants,
            'matiere': matiere,
            'prof_id': prof_id,
            'classe_id': classe_id,'prof': professeur
        })




def modifier_note(request, note_id, prof_id, classe_id):
    note = get_object_or_404(Note, pk=note_id)
    prof = get_object_or_404(Prof, id=prof_id)
    classe = get_object_or_404(Classe, id=classe_id)
    if request.method == 'POST':
        form = Notemod(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('afficher_note', prof_id=prof_id, classe_id=classe_id)
    else:
        form = Notemod(instance=note)
    return render(request, 'modifier_note.html', {'form': form, 'note': note, 'prof_id': prof_id, 'classe_id': classe_id,'prof': prof})


def supprimer_note(request, note_id, prof_id,classe_id):
    prof = get_object_or_404(Prof, id=prof_id)
    if request.method == 'POST':
        note = get_object_or_404(Note, pk=note_id)
        note.delete()
        return redirect('afficher_note', prof_id=prof_id,  classe_id=classe_id)
    else:
        # If not a POST request, show some confirmation page or redirect
        return render(request, 'confirm_delete.html', {'note_id': note_id, 'prof_id': prof_id,'classe_id': classe_id,'prof': prof})










def historique_etudiant(request, etudiant_id):
    # Obtenez tous les étudiants ayant le même CNE
    etudiants = Etudiant.objects.filter(cne=etudiant_id)
    etudiant = Etudiant.objects.filter(cne=etudiant_id).first()
    
    # Créer une liste pour stocker les informations sur l'historique académique
    historique_academique = []
    classes_suivies = []
    # Boucle sur chaque étudiant avec le même CNE
    for etudiant in etudiants:
        # Récupérer toutes les classes suivies par l'étudiant
        classes_suivies.append(etudiant.fk_classe)
        for classe in classes_suivies:
           matieres_classe = classe.matieres.all()
        
        # Initialiser la somme des notes pour cette classe
           note_generale_classe = 0
           nombre_matiere_classe = 0
        
        
        
           for matiere in matieres_classe:
            # Récupérer toutes les notes de l'étudiant pour cette matière
           
            notes_matiere = Note.objects.filter(fk_etudiant=etudiant, fk_matiere=matiere)
            
            # Calculer la somme des notes pour cette matière
            somme_notes_matiere = notes_matiere.aggregate(Sum('note'))['note__sum']
            
            # Ajouter la somme des notes de cette matière à la note générale de la classe
            if somme_notes_matiere:
                note_generale_classe += somme_notes_matiere
                nombre_matiere_classe += 1
        if nombre_matiere_classe > 0:
                note_generale_classe /= nombre_matiere_classe
                note_generale_classe = round(note_generale_classe, 2)
            
        # Ajouter les détails de cette classe à l'historique académique
        historique_academique.append({
                'classe': classe,
                
                'niveau': classe.fk_niveau.nom,  # Accéder au nom du niveau
                'annee_scolaire': classe.annee_scolaire,
                'note_generale': note_generale_classe
            })
          
        
        # Boucle sur chaque classe suivie par l'étudiant
        

    return render(request, 'historique_etudiant.html', {'historique_academique': historique_academique,'etudiant':etudiant})

 
def student_choices(request, etudiant_cne):
    etudiant = Etudiant.objects.filter(cne=etudiant_cne).first()
    choices = Choice.objects.filter(etudiant=etudiant)
    

    if choices.exists():  # Vérifie si l'étudiant a des choix existants
        if request.method == 'POST':
            for choice in choices:
                # Mettez à jour chaque choix avec les nouvelles valeurs
                choice.reason_for_choice = request.POST.get('reason_for_choice')
                choice.dream_job = request.POST.get('dream_job')
                choice.save()
            return redirect('student_choices', etudiant_cne=etudiant_cne)
        else:
            return render(request, 'student_choices.html', {'etudiant': etudiant, 'choices': choices})
    else:
        # Si l'étudiant n'a pas de choix existants, redirigez-le vers la vue d'ajout de choix
        return redirect('add_choice', etudiant_cne=etudiant_cne)
def add_choice(request, etudiant_cne):
    etudiant = Etudiant.objects.filter(cne=etudiant_cne).first()
    current_year = date.today().year
    prev_year = current_year - 1
    annee_scolaire_cible = f'{prev_year}-{current_year}'
    if etudiant.fk_classe.annee_scolaire == annee_scolaire_cible:
        niveau_actuel = etudiant.fk_classe.fk_niveau
    print( niveau_actuel)
    # Transition map, définir les niveaux accessibles après chaque niveau
    transitions = {
        "3ème année collège": ["tronc commun Scientifique", "tronc commun lettre et sciences humaines", "tronc commun technologie"],

        "tronc commun lettre et sciences humaines": ["1Bac langue arabe", "1Bac lettre et sciences humaines", "1Bac science economique et gestion","1Bac arts appliqués","1Bac chariaa"],
        "tronc commun Scientifique": ["1Bac science economique et gestion", "1Bac arts appliqués", "1Bac sciences expérimentales","1bac Sciences Mathématiques","1Bac sciences et techonologie électrique","1Bac sciences et techonologie mécanique"],
        "tronc commun technologie": ["1Bac science economique et gestion", "1Bac arts appliqués", "1Bac sciences expérimentales","1bac Sciences Mathématiques","1Bac sciences et techonologie électrique","1Bac sciences et techonologie mécanique"],

        "1Bac chariaa": ["2Bac chariaa"],
        "1Bac langue arabe": ["2Bac langue arabe"],
        "1Bac lettre et sciences humaines": ["2Bac lettre", "2Bac  sciences humaines"],
        "1Bac science economique et gestion": ["2Bac science économique", "2Bac science de gestion et comptabilité"],
        "1Bac arts appliqués": ["2Bac arts appliqués"],
        "1Bac sciences expérimentales": ["2Bac sciences de la vie et de la terre", "2Bac sciences physique chimique", "2Bac sciences agronomique"],
        "1bac Sciences Mathématiques": ["2Bac Sciences Mathématiques A", "2Bac Sciences Mathématiques B"],
        "1Bac sciences et techonologie électrique": ["2Bac sciences et techonologie électrique"],
        "1Bac sciences et techonologie mécanique": ["2Bac sciences et techonologie mécanique"],
    }

    # Obtenir les noms des niveaux suivants à partir de la carte de transitions
    niveaux_suivants_noms = transitions.get(niveau_actuel.nom, [])

    # Filtrer les niveaux disponibles basés sur la transition(objet)
    niveaux_suivants = Niveau.objects.filter(nom__in=niveaux_suivants_noms)

    if request.method == 'POST':
        # Code pour traiter la soumission du formulaire
        niveau_id = request.POST.get('niveau')
        niveau = Niveau.objects.get(id=niveau_id)
        continue_in_school = request.POST.get('continue_in_school') == 'on'

        Choice.objects.create(
            etudiant=etudiant,
            niveau=niveau,
            continue_in_school=continue_in_school,
        )
        messages.success(request, 'Choix ajouté avec succès.')
        return redirect('student_choices', etudiant_cne=etudiant.cne)

    return render(request, 'add_choice.html', {'etudiant': etudiant, 'niveaux': niveaux_suivants})

def modify_choice(request, choice_id, etudiant_cne):
    choice = get_object_or_404(Choice, id=choice_id)
    if request.method == 'POST':
        niveau_id = request.POST.get('niveau')
        continue_in_school = request.POST.get('continue_in_school') == 'on'

        niveau = Niveau.objects.get(id=niveau_id)
        choice.niveau = niveau
        choice.continue_in_school = continue_in_school
        choice.save()

        return redirect('student_choices', etudiant_cne=choice.etudiant.cne)
    
    etudiant_cne = choice.etudiant.cne
    etudiant = Etudiant.objects.filter(cne=etudiant_cne).first()
    current_year = date.today().year
    prev_year = current_year - 1
    annee_scolaire_cible = f'{prev_year}-{current_year}'
    if etudiant.fk_classe.annee_scolaire == annee_scolaire_cible:
        niveau_actuel = etudiant.fk_classe.fk_niveau
    # Transition map, définir les niveaux accessibles après chaque niveau
    transitions = {
        "3ème année collège": ["tronc commun Scientifique", "tronc commun lettre et sciences humaines", "tronc commun technologie"],

        "tronc commun lettre et sciences humaines": ["1Bac langue arabe", "1Bac lettre et sciences humaines", "1Bac science economique et gestion","1Bac arts appliqués","1Bac chariaa"],
        "tronc commun Scientifique": ["1Bac science economique et gestion", "1Bac arts appliqués", "1Bac sciences expérimentales","1bac Sciences Mathématiques","1Bac sciences et techonologie électrique","1Bac sciences et techonologie mécanique"],
        "tronc commun technologie": ["1Bac science economique et gestion", "1Bac arts appliqués", "1Bac sciences expérimentales","1bac Sciences Mathématiques","1Bac sciences et techonologie électrique","1Bac sciences et techonologie mécanique"],

        "1Bac chariaa": ["2Bac chariaa"],
        "1Bac langue arabe": ["2Bac langue arabe"],
        "1Bac lettre et sciences humaines": ["2Bac lettre", "2Bac  sciences humaines"],
        "1Bac science economique et gestion": ["2Bac science économique", "2Bac science de gestion et comptabilité"],
        "1Bac arts appliqués": ["2Bac arts appliqués"],
        "1Bac sciences expérimentales": ["2Bac sciences de la vie et de la terre", "2Bac sciences physique chimique", "2Bac sciences agronomique"],
        "1bac Sciences Mathématiques": ["2Bac Sciences Mathématiques A", "2Bac Sciences Mathématiques B"],
        "1Bac sciences et techonologie électrique": ["2Bac sciences et techonologie électrique"],
        "1Bac sciences et techonologie mécanique": ["2Bac sciences et techonologie mécanique"],
    }

    # Obtenir les noms des niveaux suivants à partir de la carte de transitions
    niveaux_suivants_noms = transitions.get(niveau_actuel.nom, [])
    # Filtrer les niveaux disponibles basés sur la transition(objet)
    niveaux_suivants = Niveau.objects.filter(nom__in=niveaux_suivants_noms)
    return render(request, 'modify_choice.html', {'choice': choice, 'niveaux': niveaux_suivants,'etudiant': etudiant })

def delete_choice(request, choice_id,etudiant_cne):
    choice = get_object_or_404(Choice, id=choice_id)
    etudiant_cne = choice.etudiant.cne
    etudiant = Etudiant.objects.filter(cne=etudiant_cne).first()
    if request.method == 'POST':
        choice.delete()
        return redirect('student_choices', etudiant_cne=etudiant_cne)
    else:
      return render(request, 'confirm_delete_choice.html', {'choice': choice,'etudiant':etudiant})






def afficher_resultat(request,etd_cne, etd_id):
   
    # Retrieve all students with the given CNE
    etudiants = Etudiant.objects.filter(cne=etd_cne)
    etudiant = get_object_or_404(Etudiant, id=etd_id)
    
    if not etudiants:
        # Handle case where no students are found
        return render(request, 'error.html', {'message': 'Aucun étudiant trouvé avec ce CNE'})

    # Retrieve all classes for these students
    classes = Classe.objects.filter(etudiant__in=etudiants).distinct()

    context = {
        'etudiants': etudiants,
        'classes': classes,
        'etudiant':etudiant,
    }
   
    return render(request, 'afficher_resultat.html', context)



def resultat(request, etd_id, semestre):
    # Fetch the student information
    if request.method == 'POST':
        annee_scolaire = request.POST.get('annee_scolaire')
        etudiant = get_object_or_404(Etudiant, id=etd_id)
    
        # Fetch the class and level information
        classe = Classe.objects.filter(annee_scolaire=annee_scolaire, etudiant=etudiant).first()
        niveau = classe.fk_niveau if classe else None
    
        # Fetch the notes for the given semester
        notes = Note.objects.filter(fk_etudiant=etudiant, semestre=semestre)
    
        # Group notes by subject
        matieres_notes = {}
        for note in notes:
            if note.fk_matiere.nom not in matieres_notes:
                matieres_notes[note.fk_matiere.nom] = []
            matieres_notes[note.fk_matiere.nom].append(note.note)
    
        # Calculate the general note for the semester
        total_notes = sum(note.note for note in notes)
        note_generale_semestre = total_notes / len(notes) if notes else 0
        note_generale_semestre = round(note_generale_semestre, 2)
        
        # Prepare context for template
        context = {
            'etudiant': etudiant,
            'niveau': niveau.nom if niveau else None,
            'annee_scolaire': classe.annee_scolaire if classe else None,
            'matiere_classe': [{
                'classe': classe,
                'matieres_notes': matieres_notes
            }],
            'semestre': semestre,
            'note_generale_semestre': note_generale_semestre
        }
    
        return render(request, 'resultat.html', context)
def logout_view(request):
    logout(request)
    return render(request, 'home.html')    
