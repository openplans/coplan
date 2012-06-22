from djangorestframework import views, permissions, status, mixins
from djangorestframework.response import ErrorResponse
from . import resources


class IsOwnerOrReadOnly (permissions.BasePermission):
    def check_permission(self, user):
        from .models import Plan
        view = self.view
        
        try:
            plan = view.get_instance()
            if view.method not in ('GET', 'HEAD') and plan.owner != user:
                raise ErrorResponse(status.HTTP_403_FORBIDDEN,
                                    {'detail': ('Only the owner of a plan may '
                                                'make modifications.')})

        except Plan.DoesNotExist:
            raise ErrorResponse(status.HTTP_404_NOT_FOUND)


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
    permissions = [IsOwnerOrReadOnly]
