# Generated by Django 5.0.4 on 2024-05-07 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='file_name',
            field=models.CharField(default='default_filename', max_length=255),
        ),
    ]