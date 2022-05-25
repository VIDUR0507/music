#from typing_extensions import self
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Song(models.Model):
    song_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=500)
    singer=models.CharField(max_length=500)
    genre=models.CharField(max_length=200)
    movie=models.CharField(max_length=500, default="")
    image=models.ImageField(upload_to='documents')
    song=models.FileField(upload_to='song_files')
    #credit=models.CharField(max_length=1000,default="")
    paginate_by = 2
                         
    def __str__(self): 
       return self.name
    
class Listenlater(models.Model):
    watch_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    video_id=models.CharField(max_length=2000, default="")

class History(models.Model):
    history_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    music_id=models.CharField(max_length=2000, default="")

class Channel(models.Model):
    channel_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=1000)
    music=models.CharField(max_length=1000)

