from django.db import models


class Plan (models.Model):
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    
    title = models.CharField(max_length=100, null=True, blank=True)
    motivation = models.CharField(max_length=140, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    owner = models.ForeignKey('auth.User', related_name='owned_plans')
    
    location_lat = models.FloatField(null=True, blank=True)
    location_lon = models.FloatField(null=True, blank=True)

    supporters = models.ManyToManyField('auth.User', 
                                        related_name='supported_plans',
                                        blank=True)


class Link (models.Model):
    plan = models.ForeignKey('coplan.Plan', related_name='links')
    url = models.URLField()


# class Image (models.Model):
#     plan = models.ForeignKey('coplan.Plan', related_name='images')
#     data = models.ImageField()


class Video (models.Model):
    plan = models.ForeignKey('coplan.Plan', related_name='videos')
    url = models.URLField()

class Comment (models.Model):
    TYPE_CHOICES = (
        (1, 'Support'),
        (-1, 'Oppose'),
        (0, 'Question'))
    
    plan = models.ForeignKey('coplan.Plan', related_name='comments')
    commenter = models.ForeignKey('auth.User', related_name='comments')
    text = models.TextField()
    type = models.IntegerField(choices=TYPE_CHOICES)
