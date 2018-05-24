from django.contrib import admin

from .models import Site, Channel, UserChannel

admin.site.register(Site)
admin.site.register(Channel)
admin.site.register(UserChannel)
