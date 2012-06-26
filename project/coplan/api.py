from djangorestframework import views, permissions, status, mixins
from djangorestframework.response import ErrorResponse
from . import models
from . import resources


class IsInstanceUserOrReadOnly (permissions.BasePermission):
    model = None
    user_attr = None
    
    def check_permission(self, user):
        view = self.view
        
        try:
            inst = view.get_instance()
            if view.method not in ('GET', 'HEAD') and \
              getattr(inst, self.user_attr) != user:
                raise ErrorResponse(
                    status.HTTP_403_FORBIDDEN,
                    {'detail': ('Only the {0} of a {1} may make '
                    'modifications.').format(self.user_attr,
                                             self.model._meta.verbose_name)})

        except self.model.DoesNotExist:
            raise ErrorResponse(status.HTTP_404_NOT_FOUND)


class IsOwnerOrReadOnly (IsInstanceUserOrReadOnly):
    model = models.Plan
    user_attr = 'owner'


class IsCommenterOrReadOnly (IsInstanceUserOrReadOnly):
    model = models.Comment
    user_attr = 'commenter'


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

class PlanCommentListView (views.ListOrCreateModelView):
    resource = resources.PlanCommentResource

class PlanCommentInstanceView (ModelInstanceMixin, views.InstanceModelView):
    resource = resources.PlanCommentResource
    permissions = [IsCommenterOrReadOnly]
