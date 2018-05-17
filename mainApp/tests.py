import requests
#from django.test import TestCase
from .models import Channel

def youtube_new_videos(channel):
    url = channel.channel_url + '/videos'
    raw_data = requests.get(url)
    start = raw_data.find('href="watch')
    print(start)

chicken = Channel.objects.filter(channel_name="LinusTechTips")
print(chicken)
youtube_new_videos(chicken)
