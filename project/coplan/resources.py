from djangorestframework import resources
from . import models

class PlanResource (resources.ModelResource):
    model = models.Plan

    # By default, id is excluded.  Override exclude to be empty.
    exclude = []

    def owner(self, plan):
        return plan.owner.pk
