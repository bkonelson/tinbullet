from django.db import models
from django.contrib.auth.models import User

class Site(models.Model):
    site_name = models.CharField(max_length=50)
    site_url = models.CharField(max_length=200)
    icon = models.CharField(max_length=100, default='genericIcon.png')
    def __str__(self):
        return self.site_name

class Channel(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=100)
    channel_url = models.CharField(max_length=200)
    channel_desc = models.CharField(max_length=300, null=True)
    channel_thumb = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.channel_name

class UserChannel(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    channels = models.ManyToManyField(Channel)
    def __str__(self):
        return self.user.username
