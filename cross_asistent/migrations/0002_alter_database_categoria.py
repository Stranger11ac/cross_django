# Generated by Django 5.0.6 on 2024-08-25 01:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cross_asistent', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='database',
            name='categoria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cross_asistent.categorias'),
        ),
    ]