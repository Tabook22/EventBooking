from django.db import models
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
from django.urls import reverse
from django.contrib.auth.models import User


class video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title=models.CharField(verbose_name='Video Title', max_length=200, null=True, blank=True)
    url=models.CharField(verbose_name='Url Address', max_length=300, null=True, blank=True)
    desc=models.TextField(verbose_name='Description')

    CATEGORY_CHOICES=[
        ("1","Programming"),
        ("2","Designing"),
        ("3","University Lectures"),
        ("4", "IoT"),
        ("5", "IT News")
        ]

    cat=models.CharField(verbose_name='Category',max_length=1, choices=CATEGORY_CHOICES, default="Programming")
    adate = models.DateField(verbose_name="Date", default=datetime.date.today)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        )


    class Meta:
        ordering=["-adate"]


    def __str__(self):
        return self.title +"-"+ self.adate.strftime('%Y')


    def get_absolute_url(self):
        return reverse('video_detail', args=[str(self.id)])

class Venue(models.Model):
    name=models.CharField('name', max_length=250, null=True, blank=True)
    address=models.CharField(max_length=300, null=True, blank=True)
    zip_code=models.CharField('Zip Code', max_length=120, null=True, blank=True)
    phone=models.CharField('contact', max_length=300, null=True, blank=True)
    web=models.URLField('Web Address', max_length=300, null=True, blank=True)
    email_address=models.EmailField('Email Address', max_length=300, null=True, blank=True)
    owner=models.IntegerField("Venue Owner", blank=False,default=1)
    venue_image=models.ImageField(null=True, blank=True, upload_to="images/")

    #list the name of each venue
    def __str__(self):
        return self.name

class myClubUser(models.Model):
    first_name=models.CharField('First Name', max_length=300, null=True, blank=True)
    last_name=models.CharField('Last Name', max_length=300, null=True, blank=True)
    email=models.EmailField('Email', max_length=300, null=True, blank=True)
    phone=models.CharField('Phone', max_length=15, null=True, blank=True)

    # List the name of the User
    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Event(models.Model):
    name=models.CharField('Event Name', max_length=250,null=True, blank=True)
    event_date=models.DateTimeField('Event Date')
    venue=models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager=models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description=models.TextField(blank=True)
    attendees=models.ManyToManyField(myClubUser, blank=True, null=True)
    approved=models.BooleanField("Approved", default=False)
    #list the name of each event
    def __str__(self):
        return self.name

    @property
    def Days_till(self):
        today=datetime.date.today()
        days_till=self.event_date.date() - today
        getDays=days_till.days
        if getDays<0:
            showResult="This Event is Past"
        else:
            showResult=getDays
        #here we want to remove the last part which comes with the date 0:00:00, because the result is:
        #is "3days,0:00:00" here i want to remove the last part from the comma
        #we convert it to string then we strip any part we need
        #here we split by comma and then we take the first part
        days_till_stripped=str(days_till).split(",",1)[0]
        return showResult

#The idea here is that each user has his own folder and his images
def get_user_image_folder(instance, filename):
    return 'images/{0}/{1}'.format(instance.user.username, filename)


class EventGallery(models.Model):
    name=models.CharField('Event Name', max_length=250,null=True, blank=True)
    event_date= models.DateField("Event Date", default=datetime.date.today)
    eventname=models.ForeignKey(Event,blank=True, null=True, on_delete=models.CASCADE)
    venuename=models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    event_image=models.ImageField(null=True, blank=True, upload_to='images/%Y/%m/%d')

    def __str__(self):
        return str(self.pk)

