from django.db import models


class Plan (models.Model):
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    
    title = models.CharField(max_length=100)
    motivation = models.CharField(max_length=140)
    details = models.TextField()
    owner = models.ForeignKey('auth.User')
    
    location_lat = models.FloatField()
    location_lon = models.FloatField()

    supporters = models.ManyToManyField('auth.User')


class Link (models.Model):
    plan = models.ForeignKey('coplan.Plan', related_name='links')
    url = models.URLField()


class Image (models.Model):
    plan = models.ForeignKey('coplan.Plan', related_name='images')
    data = models.ImageField()


class Video (models.Model):
    plan = models.ForeignKey('coplan.Plan', related_name='videos')
    url = models.URLField()
