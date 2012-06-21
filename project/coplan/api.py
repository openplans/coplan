from djangorestframework import views
from . import resources


class PlanListView (views.ListOrCreateModelView):
    resource = resources.PlanResource
    
class PlanInstanceView (views.InstanceModelView):
    resource = resources.PlanResource
