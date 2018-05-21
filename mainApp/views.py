import requests
import os
from django.shortcuts import render
from .models import Site, Channel
from apiclient.discovery import build

def index(request):
    cur_site = Site.objects.get(site_name="YouTube")
    context = {'cur_site':cur_site,}
    return render(request,'youtube/index.html', context)

def pick_channels(request):
    user_input = request.POST['input']
    channels = {}
    DEVELOPER_KEY = os.getenv("YOUTUBE_API")
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    def youtube_search():
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
        search_response = youtube.search().list(q=user_input, part="id,snippet",maxResults=5).execute()
        counter = 0
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#channel":
                channels['channel'+str(counter)] =  search_result["id"]["channelId"]
                counter += 1
    youtube_search()
    return render(request,'youtube/index.html', channels)