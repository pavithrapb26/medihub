# Generated by Django 5.1.2 on 2024-12-06 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MediHubapp', '0008_remove_medicine_companies_medicine_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='category',
            field=models.CharField(choices=[('Skincare', 'Skincare'), ('Haircare', 'Haircare'), ('Pain Relief', 'Pain Relief'), ('Vitamins', 'Vitamins')], default='Skincare', max_length=50),
            preserve_default=False,
        ),
    ]
