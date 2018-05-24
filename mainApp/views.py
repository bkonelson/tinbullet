import requests
import os
from django.shortcuts import render
from .models import Site, Channel, UserChannel
from apiclient.discovery import build
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

DEVELOPER_KEY = os.getenv("YOUTUBE_API")
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

class video():
    video_title=''
    video_url=''
    video_thumb=''
    video_channel=''

@login_required
def index(request):
    delchanname = request.POST.get('remchannel', False)
    addchanname = request.POST.get('add', False)
    if delchanname:
        ch = Channel.objects.get(channel_name=delchanname)
        UserChannel.objects.get(user=request.user).channels.remove(ch)
    if addchanname:
        ch = Channel.objects.get(channel_name=addchanname)
        UserChannel.objects.get(user=request.user).channels.add(ch)
    cur_site = Site.objects.get(site_name="YouTube")
    cur_channels = UserChannel.objects.get(user=request.user).channels.all()
    video_list = []
    if cur_channels:
        for chan in cur_channels:
            youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
            search_response = youtube.search().list(part="snippet",channelId=chan.channel_url[32:],maxResults=3,order="date",type="video").execute()
            for search_result in search_response.get("items", []):
                v=video()
                v.channel = chan
                v.video_title = search_result["snippet"]["title"]
                v.video_url = 'https://www.youtube.com/watch?v=' + search_result["id"]["videoId"]
                v.video_thumb = search_result["snippet"]['thumbnails']['default']['url']
                video_list.append(v)
    context = {'cur_site':cur_site,'video_list':video_list}
    return render(request,'youtube/index.html', context)

@login_required
def pick_channels(request):
    user_input = request.POST['input']
    context = {}
    chan_list = []
    cur_site = Site.objects.get(site_name="YouTube")
    context['cur_site'] = cur_site

    def youtube_search():
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
        search_response = youtube.search().list(q=user_input, part="id,snippet",maxResults=5,type="channel").execute()           
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#channel":
                c = Channel()
                c.site = Site.objects.get(site_name="YouTube")
                c.channel_url = 'https://www.youtube.com/channel/' + search_result["id"]["channelId"]
                c.channel_name =  search_result["snippet"]['title']
                c.channel_desc =  search_result["snippet"]['description']
                c.channel_thumb =  search_result["snippet"]['thumbnails']['default']['url']
                chan_list.append(c)
                try: 
                    Channel.objects.get(channel_name = c.channel_name)
                except:
                    c.save()
        context['channels'] = chan_list
    youtube_search()
    return render(request,'youtube/channelpick.html', context)