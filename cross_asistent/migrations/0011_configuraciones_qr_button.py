# Generated by Django 5.0.6 on 2024-09-04 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cross_asistent', '0010_galeria_delete_imagenes'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuraciones',
            name='qr_button',
            field=models.BooleanField(default=True),
        ),
    ]
