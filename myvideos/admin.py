from django.contrib import admin
from .models import video,Event, Venue, myClubUser, EventGallery

# Register your models here.
admin.site.register(Venue)
admin.site.register(video)
admin.site.register(Event)
admin.site.register(myClubUser)
admin.site.register(EventGallery)