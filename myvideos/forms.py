from django import forms
from django.forms import ModelForm
from .models import video, Venue, Event, EventGallery

#This class used for datapicker in the forms, here we need to add a datepicker in the form
#There is also a short answer insted of using the class
# 'event_date':forms.TextInput(attrs={'class':'form-control', 'placeholder':'attendees','type': 'date'}),

class DateInput(forms.DateInput):
    input_type='date'

#Event Form
#This for is for the supper user and he can see all the list of the managers, not like the user form
class EventFormAdmin(ModelForm):
    class Meta:
        model =Event
        fields=('name','event_date','venue','manager','attendees','description')
        #here we want to get rid of all the labels
        labels={
           'name':'Name',
           'event_date': 'Event Date',
           'venue': 'Event Venue',
           'manager': 'Event Manager',
           'attendees':'Attendess',
            'description':'Description',
            }
        widgets ={
            'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'name'}),
            #this is important format=('%Y-%m-%d') is important to prevent not showing the initial date when updating the data
            'event_date':DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control','placeholder':'event_date'}),
            'venue':forms.Select(attrs={'class':'form-select','placeholder':'venue'}),
            'manager':forms.Select(attrs={'class':'form-select', 'placeholder':'manager'}),
            'attendees':forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'attendees'}),
            'description':forms.Textarea(attrs={'class':'form-control', 'placeholder':'description'}),
            }



#User Evnent Form
#In this form we removed the manger field from it, because we don't want to allow the user to change the manager
#The manager is the user who logged in, and we want't it to be like that be default
class EventForm(ModelForm):
    class Meta:
        model =Event
        fields=('name','event_date','venue','attendees','description')
        #here we want to get rid of all the labels
        labels={
           'name':'Name',
           'event_date': 'Event Date',
           'venue': 'Event Venue',
           'attendees':'Attendess',
           'description':'Description',
            }
        widgets ={
            'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'name'}),
             #this is important format=('%Y-%m-%d') is important to prevent not showing the initial date when updating the data
            'event_date':DateInput(format=('%Y-%m-%d'),  attrs={'class':'form-control','placeholder':'event_date'}),
            'venue':forms.Select(attrs={'class':'form-select','placeholder':'venue'}),
            'attendees':forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'attendees'}),
            'description':forms.Textarea(attrs={'class':'form-control', 'placeholder':'description'}),
            }
        #even_date=forms.DateField(widget=DateInput)

#VideoForm
class VideoForm(ModelForm):
    class Meta:
        model =video
        #fields="__all__")
        fields=('title','url','desc','cat','adate','rating')

#Event Gallery form
class EventGalleryForm(ModelForm):
    class Meta:
        model =EventGallery
        fields=('name','event_date','eventname','venuename')
        labels={'name':'','event_date':'','event name':'','venu name':''}
        Widgets={
            'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'name'}),
            'event_date':DateInput(format=('%Y-%m-%d'),  attrs={'class':'form-control','placeholder':'event_date'}),
            'eventname':forms.Select(attrs={'class':'form-select','placeholder':'event'}),
            'venuename':forms.Select(attrs={'class':'form-select','placeholder':'venue'}),
            }

#Venue Form
class VenueForm(ModelForm):
    class Meta:
        model =Venue
        fields=('name','address','zip_code','phone','web','email_address','venue_image')
        #here we want to get rid of all the labels
        labels={
           'name':'',
           'address': '',
           'zip_code': '',
           'phone': '',
            'web':'',
            'email_address':'',
            'venue_image':'',
            }
        widgets ={
            'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'name'}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':'address'}),
            'zip_code':forms.TextInput(attrs={'class':'form-control','placeholder':'zip_code'}),
            'phone':forms.TextInput(attrs={'class':'form-control', 'placeholder':'phone'}),
            'web':forms.TextInput(attrs={'class':'form-control', 'placeholder':'web'}),
            'email_address':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'email_address'}),
            }