from django.db import models
from django.contrib.auth import models as auth


class Planner (auth.User):
    class Meta:
        proxy = True

    @property
    def avatar_url(self):
        from random import randint
        return ''.join(['/static/coplan/img/user', str(randint(1,4)), '.png'])

        
class Plan (models.Model):
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    
    title = models.CharField(max_length=100, null=True, blank=True)
    motivation = models.CharField(max_length=140, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    owner = models.ForeignKey('coplan.Planner', related_name='owned_plans')
    
    location_lat = models.FloatField(null=True, blank=True)
    location_lon = models.FloatField(null=True, blank=True)

    supporters = models.ManyToManyField('coplan.Planner', 
                                        related_name='supported_plans',
                                        through='coplan.Support',
                                        blank=True)


class Support (models.Model):
    MOTIVATION_CHOICES = (
        ('I live here', 'I live here'),
        ('I work here', 'I work here'),
        ('I play here', 'I play here'))
    supporter = models.ForeignKey('coplan.Planner', related_name='support')
    plan = models.ForeignKey('coplan.Plan', related_name='support')
    motivation = models.CharField(max_length=140, choices=MOTIVATION_CHOICES,
                                  help_text='What is your connection to the area?')

    class Meta:
        unique_together = [('supporter', 'plan'),]

    
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
    commenter = models.ForeignKey('coplan.Planner', related_name='comments')
    text = models.TextField()
    type = models.IntegerField(choices=TYPE_CHOICES)
    created_datetime = models.DateTimeField(auto_now_add=True)
