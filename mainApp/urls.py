from django.urls import path
from . import views

app_name = 'mainApp'
urlpatterns = [
    path('', views.index, name = 'index',),
    path('pickchannels/', views.pick_channels, name='pickchannels'),
]