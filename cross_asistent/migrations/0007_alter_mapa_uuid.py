# Generated by Django 5.0.6 on 2024-08-26 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cross_asistent', '0006_alter_database_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapa',
            name='uuid',
            field=models.CharField(max_length=25),
        ),
    ]