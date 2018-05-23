import requests
import os
from django.shortcuts import render
from .models import Site, Channel
from apiclient.discovery import build
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    cur_site = Site.objects.get(site_name="YouTube")
    context = {'cur_site':cur_site,}
    return render(request,'youtube/index.html', context)

@login_required
def pick_channels(request):
    user_input = request.POST['input']
    context = {}
    chan_list = []
    cur_site = Site.objects.get(site_name="YouTube")
    context['cur_site'] = cur_site
    DEVELOPER_KEY = os.getenv("YOUTUBE_API")
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    def youtube_search():
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
        search_response = youtube.search().list(q=user_input, part="id,snippet",maxResults=50).execute()           
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#channel":
                c = Channel()
                c.site = Site.objects.get(site_name="YouTube")
                c.channel_url = 'https://www.youtube.com/channel/' + search_result["id"]["channelId"]
                c.channel_name =  search_result["snippet"]['title']
                c.channel_desc =  search_result["snippet"]['description']
                c.channel_thumb =  search_result["snippet"]['thumbnails']['default']['url']
                chan_list.append(c)

        context['channels'] = chan_list
    youtube_search()
    return render(request,'youtube/channelpick.html', context)