from django.db import models

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
    def __str__(self):
        return self.channel_name


