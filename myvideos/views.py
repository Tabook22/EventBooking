import json
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import calendar
from calendar import HTMLCalendar
from .forms import VideoForm, VenueForm, EventForm, EventFormAdmin, EventGalleryForm
from datetime import datetime
from .models import Event,Venue, EventGallery
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse,FileResponse
from django.core import serializers
import csv
from django.contrib import messages

#these are the libraries we need to work with to generate PDF file
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.db.models import Q
#Import Paginaiton Stuff
from django.core.paginator import Paginator, EmptyPage

# Delete All images 
def detleteallimages(request, getname):
    #here we are going to delete more than one object that is why we used filter() method
    allimg=EventGallery.objects.all().filter(name=getname)
    collname=getname #storing the gallery collection name to send it back to the managegallery.html
    #here we are looping through the selecte objects with gallery collection name getname
    for img in allimg:
        img.delete()
        
    messages.success(request,"All Images in the Gallery Collections were deleted successfully for collection "+getname)
    img_list=EventGallery.objects.all().order_by('-event_date')
    #To get only the distinct names of the event gallery
    evn_list=EventGallery.objects.all().values('name').distinct()
    template_name='gallery/managegallery.html'
    return render(request,template_name,{'img_list':img_list,
                                                'evn_list':evn_list,'getname':'nogallery','collname':"All Images In The Gallery"
                                                }
                        )
    #return redirect('home')



#Here we are going to manage the uploaded images
def manageGallery(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            #values = request.POST.getlist('result') or request.POST.get('result) or request.POST['result']
            getname=request.POST.get("selevent")

            #here we need to filter the EventGallery get more than one value, that is why we use filter,
            #we choose to get the first one, because the resut is just a repetion
            #the result will be a tuple
            getevent=EventGallery.objects.all().filter(name=getname).values_list('eventname','event_date','venuename').first()

            #because the result is a tuble that is why we use the indexes 0, 1 to get the first and second values
            getevntname=getevent[0]
            geteventdate=getevent[1]
            getvenuename=getevent[2]
            
            #complex queries, to filter by eventname and date, show only images with the same event gallery and same date
            img_list=EventGallery.objects.filter (Q(eventname=getevntname) & Q(event_date=geteventdate))

            #To get only the distinct names of the event gallery
            evn_list=EventGallery.objects.all().values('name').distinct()
        
        
            
            #Get the number of images in each gallery event
            img_count=img_list.count()
            #get event detaisl;
            eventdetails=Event.objects.get(pk=getevntname)
            #get venue detaisl;
            venuedetails=Venue.objects.get(pk=getvenuename)
            template_name='gallery/managegallery.html'
            return render(request, template_name,{'img_list':img_list,
                                                'evn_list':evn_list,
                                                'img_count':img_count,
                                                'getname':getname,
                                                'geteventdate':geteventdate,
                                                'eventdetails':eventdetails.name,
                                                'venuedetails':venuedetails.name,
                                                'collname':getname,
                                                }
                        )
        else:
            img_list=EventGallery.objects.all().order_by('-event_date')
            #To get only the distinct names of the event gallery
            evn_list=EventGallery.objects.all().values('name').distinct()
            template_name='gallery/managegallery.html'
            return render(request, template_name,{'img_list':img_list,
                                                'evn_list':evn_list,'getname':'nogallery'
                                                }
                        )
            
    else:
        messages.success(request,("You are not authroized to view this page !!"))
        return redirect('home')
            
    pass
    
    
#Search for specific gallery 
def showgallery(request):
    # request should be POST
    if request.method == "POST":
        #values = request.POST.getlist('result') or request.POST.get('result) or request.POST['result']
        getname=request.POST.get("selevent")

        #here we need to filter the EventGallery get more than one value, that is why we use filter,
        #we choose to get the first one, because the resut is just a repetion
        #the result will be a tuple
        getevent=EventGallery.objects.all().filter(name=getname).values_list('eventname','event_date','venuename').first()

        #because the result is a tuble that is why we use the indexes 0, 1 to get the first and second values
        getevntname=getevent[0]
        geteventdate=getevent[1]
        getvenuename=getevent[2]
        
        #complex queries, to filter by eventname and date, show only images with the same event gallery and same date
        img_list=EventGallery.objects.filter (Q(eventname=getevntname) & Q(event_date=geteventdate))

        #To get only the distinct names of the event gallery
        evn_list=EventGallery.objects.all().values('name').distinct()
    
      
        
        #Get the number of images in each gallery event
        img_count=img_list.count()
        #get event detaisl;
        eventdetails=Event.objects.get(pk=getevntname)
        #get venue detaisl;
        venuedetails=Venue.objects.get(pk=getvenuename)
        template_name='gallery/gallerylist.html'
        return render(request, template_name,{'img_list':img_list,
                                              'evn_list':evn_list,
                                              'img_count':img_count,
                                              'getname':getname,
                                              'geteventdate':geteventdate,
                                              'eventdetails':eventdetails.name,
                                              'venuedetails':venuedetails.name,
                                              }
                      )
        
        
#Image Gallery View------------------------------------------------------
def galleryview(request):
    if request.method=="POST":
        pass
    else:
        form=EventGalleryForm
        template_name='gallery/main.html'
        return render(request, template_name, {'form':form})


#Image Gallery File Upload
def file_upload_view(request):
    if request.method=='POST':
        form=EventGalleryForm(request.POST, request.FILES or None)

        #To access all items in a MultiValueDict, you use .get('file'),
        #it is important to know that Django automatically handles multiple
        #inputs how have the same name, in such case it hands your code a list of values
        #instead of a single value.
        print(request.FILES)
        my_file=request.FILES.get('file')
        if form.is_valid():
            eventimg=form.save(commit=False)
            eventimg.event_image=my_file
            eventimg.save()
           # return HttpResponseRedirect('/')
        else:
            return HttpResponse('Thank Allah more merci more mercifull')

    return JsonResponse({'post':'false'})



#Show Gallery List --------------------------------------------------------------------
def gallerylist(request):
     #get all the images
    evn_list=EventGallery.objects.all().values('name').distinct()
    #evn_list=EventGallery.objects.all()
    img_list=EventGallery.objects.all()

    #Get counts
    img_count=EventGallery.objects.all().count()

    img_list=EventGallery.objects.all().order_by('-event_date')
    template_name='gallery/gallerylist.html'
    return render(request, template_name,{'img_list':img_list,'evn_list':evn_list,'img_count':img_count})


#Show single event
def show_event(request, event_id):
    event= Event.objects.get(pk=event_id)
    return render(request, "events/show_event2.html",{"event":event})

#Show the events which related to a particular venue
def venue_events(request, venue_id):
    #Grab the venue
    venue=Venue.objects.get(id=venue_id)
    #Grab the events from that venue
    events=venue.event_set.all()

    if events:
        return render(request, "events/venue_events.html",{"events":events})
    else:
        messages.success(request,"This Venue Has No Events At This Time")
        return redirect('admin-approval')

#Admin approval main event
def adminapproval(request):
    #Get the Venues
    venue_list=Venue.objects.all()

    #Get counts
    event_count=Event.objects.all().count()
    venue_count=Venue.objects.all().count()
    user_count=User.objects.all().count()

    event_list=Event.objects.all().order_by('-event_date')
    if request.user.is_superuser:
        if request.method=="POST":
            #store the checked boxes ids in a list called id_list
            id_list=request.POST.getlist('boxes') #get the id list of the checkbox

            #Uncheck all events,and we checked only those boxed who are passed checked from the form, we do this to overcome the problem of unchecked boxes, because in this case nontihging will be passed to the view
            event_list.update(approved=False)

            #update the database, we are going through the list of checked boxed and updated the database
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved=True)
            messages.success(request,"Event List Approved Successfuly")
            return redirect('home')


        else:
            return render(request,'events/admin_approval.html',
            {"event_list":event_list,
            "event_count":event_count,
            "venue_count":venue_count,
            "user_count":user_count,
            "venue_list":venue_list})
    else:
        messages.success(request,"You are not authorized to see this page")
        return redirect('home')

    return render(request,'events/admin_approval.html')

#My Events page
def my_events(request):
    if request.user.is_authenticated:
        #return the current user id
        me=request.user.id
        events =Event.objects.filter(attendees=me)
        return render(request,
        'events/my_events.html',
        {'events':events}
        )
    else:
        messages.success(request,("You are not authroized to view this page !!"))
        return redirect('home')

#Generate a PDF for venues---------------------
def venuePdf(request):
    #Create Bytestream buffer
    buf=io.BytesIO()
    #Creaate a canvas
    c=canvas.Canvas(buf, pagesize=letter, bottomup=0)
    #Create a text object
    textob=c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica", 14)

    #Add some line of text
    #lines=[
    #    "This is line 1",
    #    "This is line 2",
    #    "This is line 3",
    #    ]

    #Get all the items from Venue
    venues=Venue.objects.all()

    #Create blank list
    lines=[]

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append("------------------------------------")
    #loop
    for line in lines:
        textob.textLine(line)

    #Finish Up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    #Return something
    return FileResponse(buf, as_attachment=True, filename='venue_pdf.pdf')

#Generate a CSV for venues---------------------
def venueCsv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment;filename=venues.csv'

    #Create a csv writer
    writer=csv.writer(response)

    #Get all Items for object Venue
    venues=Venue.objects.all()

    #Add column headings to the csv file
    writer.writerow(['Venu Name','Address','Zip Code','Phone','Web Address', 'Email'])

    #loop through the items
    for venue in venues:
        writer.writerow([venue.name,venue.address,venue.zip_code,venue.phone,venue.web,venue.email_address])


    return response

#Generate a text file for venues---------------------
def venueText(request):
    response=HttpResponse(content_type='text/plain')
    response['Content-Disposition']='attachment;filename=venues.txt'

    #Get all Items for object Venue
    venues=Venue.objects.all()

    #create a blank list
    lines=[]

    #loop through the items
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.zip_code}{venue.phone}\n{venue.web}\n{venue.email_address}\n\n')

    #Write to textfile
    response.writelines(lines)
    return response

#Delete an Event-------------------------------------
def deleteEvent(request, event_id):
    event=Event.objects.get(pk=event_id)
    #Here we getting the event manager and making sure he is the one who is deleting this event
    if request.user==event.manager:
        event.delete()
        messages.success(request,("Event Deleted...!!!"))
        return redirect('list-events')
    else:
        messages.success(request,("You can't delete this event, you are not authroized!!"))
        return redirect('list-events')
#Delete an Venue-------------------------------------
def deleteVenue(request, venue_id):
    venue=Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')

# List of Venuens--------------------------------------
def listVenues(request):
    #Set up Pagination
    #Here we need two Items per page
    p=Paginator(Venue.objects.all(),2)
    #Keep track of the page
    #Here each time we make a rquest to that page we need to get that page, that is way we wrote GET, get
    #Here also we can descide where to start pagination for example:
    #page=request.GET.get('page',2), here we decided to start from patg2
    page=request.GET.get('page')

    #Here we try to solve an issue if we try to go to a page which didn't exist
    try:
        venues=p.get_page(page)
    except EmptyPage:
        venues=p.get_page(1)
    venues=p.get_page(page)

    return render(request, 'events/venues.html',{
    'venues':venues})

# Show venue-------------------------------------------
def show_venue(request, venue_id):
    #get a particular venue
    venue=Venue.objects.get(pk=venue_id)
    #getting the owner of this venue, because we know the owner is the user who is eneter that data
    venue_owner=User.objects.get(pk=venue.owner)
    #The idea here is get the name of the owner and displaying it in the form
    return render(request, 'events/show_venue.html',{
        'venue':venue,
        'venue_owner':venue_owner})

#Update Venues--------------------------------------
def updateVenue(request, venue_id):
    venue=Venue.objects.get(pk=venue_id)
    #here we are getting an instance of venue and add it to the form, notice we have also FILES in the form which we requesting
    form=VenueForm(request.POST or None,request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')
    return render(request, 'events/update_venue.html',{
        'venue':venue,'form':form})

#Update Events--------------------------------------
def updateEvent(request, event_id):
    event=Event.objects.get(pk=event_id)
    #here we first checking to see if the user is a superuser or not, because we have two types
    # of forms one for the superuser and the othe for the normal uses
    if request.user.is_superuser:
        #here we are getting an instance of the event and adding it to the form
        form=EventFormAdmin(request.POST or None, instance=event)
    else:
        #here we are getting an instance of the event and adding it to the form
        form=EventForm(request.POST or None, instance=event)

    if form.is_valid():
        form.save()
        return redirect('list-events')

    return render(request, 'events/update_event.html',{
        'event':event,'form':form})

#Search Venues--------------------------------------
def searchVenues(request):
    if request.method=="POST":
        searched=request.POST['searched']
        venues=Venue.objects.filter(name__icontains=searched)
        thereResults=False
        if len(venues) !=0:
            thereResults=True
            return render(request,'events/search_venues.html',{
            'thereResults':thereResults,
            'searched':searched,
            'venues':venues,
            })
        else:
            msg="Sorry, There is no result...."
            return render(request,'events/search_venues.html',{
            'thereResults':thereResults,
            'searched':searched,
            'msg':msg,
            })
    else:
        msg="....Please Search for a Venue...."
        return render(request,'events/search_venues.html',{'msg':msg,})

def searchEvents(request):
    if request.method=="POST":
        searched=request.POST['searched']
        #here we are going to use description field in Event table to search in, because it is more descriptive
        events=Event.objects.filter(description__icontains=searched)
        thereResults=False
        if len(events) !=0:
            thereResults=True
            return render(request,'events/search_events.html',{
            'thereResults':thereResults,
            'searched':searched,
            'events':events,
            })
        else:
            msg="Sorry, There is no result...."
            return render(request,'events/search_events.html',{
            'thereResults':thereResults,
            'searched':searched,
            'msg':msg,
            })
    else:
        msg="....Please Search for an Event...."
        return render(request,'events/search_events.html',{'msg':msg,})

# Events-----------------------------------------------------------------
def all_events(request):
    #get all the events by event date
    #event_list=Event.objects.all().order_by('event_date')
    #get all the events in ascending order, to make it in decending just add "-" befor event_date to be "-event_date"
    event_list=Event.objects.all().order_by('-event_date')
    return render(request, 'event_list.html',{
        "event_list":event_list,
        })

#Add Events---------------------------------------------------------------
def addEvent(request):
    submitted=False
    if request.method=="POST":
        #Here we we have two types of forms one to be filled by the superuser and the other to be filled by the users
        #We make two forms to prevent the user, from modifying the event manager, and keep that only to the superuser
        #First we need to check to see if the user is a supperuser
        if request.user.is_superuser:
            form=EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/videos/add_event?submitted=True')
        else:
            form=EventForm(request.POST)
            if form.is_valid():
                event=form.save(commit=False) # stope saving now and wite, because new data will be added below, befor saving the form
                event.manager=request.user # Here we are adding the user name, which comes with request
                event.save()
                return HttpResponseRedirect('/videos/add_event?submitted=True')
    else:
        #Here we are going to page and displying form, to fill it with data
        if request.user.is_superuser:
            form=EventFormAdmin
        else:
            form=EventForm

        if 'submitted' in request.GET:
            submitted=True

    form=EventFormAdmin
    return render(request, 'events/add_event.html', {'form':form, 'submitted':submitted})

#Add Venue--------------------------------------
def addVenue(request):
    submitted=False
    if request.method=="POST":
        #here in addition to posted data main text, we also dealing with images
        #so we have two types of request, text and files
        form=VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue=form.save(commit=False) #This means, don't save the data yet, I will save it later
            venue.owner=request.user.id #This means, the owner filed, fill it with the data of othe user, which comes with the rquest, and from that that we need the "user id"
            venue.save() #now save the data after adding the user id
            return HttpResponseRedirect('/videos/add_venue?submitted=True')
    else:
        form=VenueForm
        if 'submitted' in request.GET:
            submitted=True

    return render(request, 'events/add_venue.html', {'form':form, 'submitted':submitted})

# Home page--------------------------------------
#here we need to give a default year and month when we started the home view
#datetime.now().year the current year, datetime.now().strftime('%B) the current month
def home(request,year=datetime.now().year, month=datetime.now().strftime('%B')):
    #convert month to upercase, this importnat, because uppercase might cause error
    month=month.capitalize()
    #convert month from name to number
    month_number=list(calendar.month_name).index(month)
    #convert it to an integer
    month_number=int(month_number)

    #Get the current year
    now=datetime.now()
    current_year=now.year


    #Search for dates
    event_list=Event.objects.filter(
        event_date__year=year).filter(
        event_date__month=month_number
        )


    #get current time
    time=now.strftime('%I:%M %p')
    #create a calender
    cal=HTMLCalendar().formatmonth(year, month_number)
    return render(request,'home.html',{
        "year":year,
        "month":month,
        "cal":cal,
        "current_year":current_year,
        "time":time,
        "event_list":event_list,
        })

# Create your views here.
def videos(request):
    return render(request,'videos/videolst.html')

# Add new video--------------------------------------
def addVideos(request):
    submitted=False
    if request.method=="POST":
        form=VideoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/videos/addvideo?submitted=True')
    else:
        form=VideoForm
        if 'submitted' in request.GET:
            submitted=True

    return render(request, 'videos/add_video.html', {'form':form, 'submitted':submitted})

# list video--------------------------------------
def listVideos(request):
    return render(request, 'videos/video_list.html')