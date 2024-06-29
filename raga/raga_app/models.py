from django.db import models
from django.conf import settings

# Create your models here.
class Audio(models.Model):
    title = models.CharField(max_length=100)
    audio = models.FileField(upload_to='audio/')
    uploaded_date = models.DateTimeField(auto_now_add=True)

    title1 = models.CharField(max_length=100,default='null')
    audio1 = models.FileField(upload_to='swara/')
    uploaded_date1 = models.DateTimeField(auto_now_add=True)

    CHOICES = [
        ('song', 'Song'),
        ('swara', 'Swara'),
    ]
    selected_option = models.CharField(max_length=20, choices=CHOICES,default='song',blank=False)
    