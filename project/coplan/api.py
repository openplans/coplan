from djangorestframework import views, mixins
from . import permissions
from . import resources


class ModelInstanceMixin (mixins.ModelMixin):
    """ Overrides the ModelMixin.get_instance to assume a single instance for
    the view.  Caches the instance object.
    """
    
    def get_instance(self, **kwargs):
        if not hasattr(self, '_instance'):
            query_kwargs = kwargs or self.get_query_kwargs(
                self.request, *self.args, **self.kwargs)
            self._instance = super(ModelInstanceMixin, self).get_instance(
                **query_kwargs)
        return  self._instance

    
class PlanListView (views.ListOrCreateModelView):
    resource = resources.PlanResource
    
class PlanInstanceView (ModelInstanceMixin, views.InstanceModelView):
    resource = resources.PlanResource
    permissions = [permissions.IsOwnerOrReadOnly]

class PlanCommentListView (views.ListOrCreateModelView):
    resource = resources.PlanCommentResource

class PlanCommentInstanceView (ModelInstanceMixin, views.InstanceModelView):
    resource = resources.PlanCommentResource
    permissions = [permissions.IsCommenterOrReadOnly]
