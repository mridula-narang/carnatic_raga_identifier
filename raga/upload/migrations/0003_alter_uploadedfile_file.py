# Generated by Django 5.0.4 on 2024-05-07 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0002_uploadedfile_file_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfile',
            name='file',
            field=models.FileField(upload_to='audio/'),
        ),
    ]
