# Generated by Django 5.1.2 on 2024-12-01 19:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MediHubapp', '0007_remove_medicine_company_medicine_companies'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicine',
            name='companies',
        ),
        migrations.AddField(
            model_name='medicine',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='medicines', to='MediHubapp.company'),
            preserve_default=False,
        ),
    ]
