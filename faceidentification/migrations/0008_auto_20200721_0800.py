# Generated by Django 3.0.8 on 2020-07-21 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faceidentification', '0007_auto_20200721_0739'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='access_status',
            table='access',
        ),
        migrations.AlterModelTable(
            name='info_about_face',
            table='journal',
        ),
    ]
