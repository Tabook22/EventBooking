from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('add_venue/', views.addVenue, name='add_venue'),
    path('add_event', views.addEvent, name='add-event'),
    path('update_venue/<venue_id>', views.updateVenue, name='update-venue'),
    path('update_event/<event_id>', views.updateEvent, name='update-event'),
    path('addvideo/', views.addVideos, name="addvideo"),
    path('<int:year>/<str:month>/', views.home, name="home"),
    path('listvideos/', views.listVideos, name="videolst"),
    path('events/', views.all_events, name='list-events'),
    path('venues/', views.listVenues, name='list-venues'),
    path('show_venue/<venue_id>', views.show_venue, name='show-venue'),
    path('searchvenues',views.searchVenues, name='search-venues'),
    path('delete_event/<event_id>',views.deleteEvent, name='delete-event'),
    path('delete_venue/<venue_id>',views.deleteVenue, name='delete-venue'),
    path('venue_text/', views.venueText, name='venue-text'),
    path('venue_csv/', views.venueCsv,name='venue-csv'),
    path('venue_pdf',views.venuePdf, name='venue-pdf'),
    path('my_events',views.my_events, name='my-events'),
    path('searchevents',views.searchEvents, name='search-events'),
    path('adminapproval',views.adminapproval, name='admin-approval'),
    path('venue_events/<venue_id>', views.venue_events, name='venue-events'),
    path('show_event/<event_id>', views.show_event, name='show-event'),
    path('gallery', views.galleryview, name='gallery-view'),
    path('upload/', views.file_upload_view, name='upload-view'),
]