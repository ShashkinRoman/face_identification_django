# Generated by Django 3.0.8 on 2020-07-23 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faceidentification', '0012_auto_20200723_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='access_status',
            name='path_download',
            field=models.ImageField(upload_to='media/'),
        ),
    ]
