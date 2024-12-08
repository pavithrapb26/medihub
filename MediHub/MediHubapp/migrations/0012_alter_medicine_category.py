# Generated by Django 5.1.2 on 2024-12-07 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MediHubapp', '0011_customer_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='category',
            field=models.CharField(choices=[('Skincare', 'Skincare'), ('Haircare', 'Haircare'), ('Pain Relief', 'Pain Relief'), ('Vitamins', 'Vitamins'), ('General medicine', 'General medicines')], max_length=50),
        ),
    ]
