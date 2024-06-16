from django.db import models
from authentification.models import User
class Album(models.Model):
    title = models.CharField(max_length=120)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    cover = models.ImageField(upload_to="covers")
    

class Track(models.Model):
    title = models.CharField(max_length=80)
    album = models.ForeignKey(Album,on_delete=models.CASCADE)
    likes=models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    rec = models.FileField(upload_to="music",null=True)
    streams = models.PositiveIntegerField(default=0)

class Like(models.Model):
    liked_by = models.ForeignKey(User,on_delete=models.CASCADE)
    track = models.ForeignKey(Track,on_delete=models.CASCADE)

class DisLike(models.Model):
    disliked_by = models.ForeignKey(User,on_delete=models.CASCADE)
    track = models.ForeignKey(Track,on_delete=models.CASCADE)

