# Generated by Django 5.0.4 on 2024-04-21 22:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tawjihi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='classe',
            name='professeur',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app_tawjihi.prof'),
        ),
        migrations.AddField(
            model_name='matiere',
            name='professeur',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app_tawjihi.prof'),
        ),
    ]
