# Generated by Django 4.0.2 on 2022-03-21 06:51

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='myClubUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=300, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=300, null=True, verbose_name='Last Name')),
                ('email', models.EmailField(blank=True, max_length=300, null=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Phone')),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True, verbose_name='name')),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=120, null=True, verbose_name='Zip Code')),
                ('phone', models.CharField(blank=True, max_length=300, null=True, verbose_name='contact')),
                ('web', models.URLField(blank=True, max_length=300, null=True, verbose_name='Web Address')),
                ('email_address', models.EmailField(blank=True, max_length=300, null=True, verbose_name='Email Address')),
                ('owner', models.IntegerField(default=1, verbose_name='Venue Owner')),
                ('venue_image', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='video',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Video Title')),
                ('url', models.CharField(blank=True, max_length=300, null=True, verbose_name='Url Address')),
                ('desc', models.TextField(verbose_name='Description')),
                ('cat', models.CharField(choices=[('1', 'Programming'), ('2', 'Designing'), ('3', 'University Lectures'), ('4', 'IoT'), ('5', 'IT News')], default='Programming', max_length=1, verbose_name='Category')),
                ('adate', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('rating', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)])),
            ],
            options={
                'ordering': ['-adate'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Event Name')),
                ('event_date', models.DateTimeField(verbose_name='Event Date')),
                ('description', models.TextField(blank=True)),
                ('attendees', models.ManyToManyField(blank=True, null=True, to='myvideos.myClubUser')),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('venue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myvideos.venue')),
            ],
        ),
    ]