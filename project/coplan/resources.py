from djangorestframework import resources
from . import models

class PlanResource (resources.ModelResource):
    model = models.Plan
    fields = ['owner', 
              'created_datetime', 
              'updated_datetime', 
              'title', 
              'motivation', 
              'details',
              'id',
              'url',]

    def owner(self, plan):
        return plan.owner.pk
