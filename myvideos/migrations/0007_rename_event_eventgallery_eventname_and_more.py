# Generated by Django 4.0.2 on 2022-04-16 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myvideos', '0006_alter_eventgallery_event_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventgallery',
            old_name='event',
            new_name='eventname',
        ),
        migrations.RenameField(
            model_name='eventgallery',
            old_name='venue',
            new_name='venuename',
        ),
    ]