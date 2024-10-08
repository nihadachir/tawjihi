# Generated by Django 5.0.4 on 2024-04-30 16:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_tawjihi', '0009_remove_classe_fk_niveau_remove_classe_professeur_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('nombre_etudiant', models.IntegerField()),
                ('annee_scolaire', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Matiere',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Niveau',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Etudiant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('cne', models.CharField(max_length=10, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('nom_tuteur', models.CharField(max_length=100)),
                ('telephone', models.CharField(max_length=10)),
                ('date_naissance', models.DateField()),
                ('fk_classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_tawjihi.classe')),
            ],
        ),
        migrations.AddField(
            model_name='classe',
            name='fk_niveau',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_tawjihi.niveau'),
        ),
        migrations.CreateModel(
            name='Prof',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('mail', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=100)),
                ('matiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_tawjihi.matiere')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.FloatField()),
                ('semestre', models.IntegerField()),
                ('fk_etudiant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_tawjihi.etudiant')),
                ('fk_matiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_tawjihi.matiere')),
                ('fk_prof', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_tawjihi.prof')),
            ],
        ),
        migrations.AddField(
            model_name='classe',
            name='professeur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_tawjihi.prof'),
        ),
    ]
