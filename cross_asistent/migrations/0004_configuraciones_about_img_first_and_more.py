# Generated by Django 5.0.6 on 2024-08-25 20:36

import cross_asistent.models
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cross_asistent', '0003_configuraciones_alter_banners_redirigir_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuraciones',
            name='about_img_first',
            field=models.ImageField(default='primer texto', upload_to=cross_asistent.models.set_conf_path),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configuraciones',
            name='about_img_second',
            field=models.ImageField(default='primer imagen', upload_to=cross_asistent.models.set_conf_path),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configuraciones',
            name='about_text_first',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configuraciones',
            name='about_text_second',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configuraciones',
            name='calendar_btnsYear',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='configuraciones',
            name='copyright_year',
            field=models.CharField(default='2020', max_length=50),
        ),
        migrations.AddField(
            model_name='configuraciones',
            name='redes_sociales',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='configuraciones',
            name='utc_link',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='configuraciones',
            name='qr_image',
            field=models.ImageField(default='on', upload_to=cross_asistent.models.set_conf_path),
            preserve_default=False,
        ),
    ]
