from django.shortcuts import render
from .models import Site

def index(request):
    cur_site = Site.objects.get(site_name="YouTube")
    context = {'cur_site':cur_site}
    return render(request,'youtube/index.html', context)
