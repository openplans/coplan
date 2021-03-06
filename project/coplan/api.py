from django.db import IntegrityError
from djangorestframework import views, mixins, status
from djangorestframework.response import ErrorResponse
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

    def get_instance_data(self, model, content, **kwargs):
        """Get the commenting user as the one that is logged in."""
        data = super(PlanCommentListView, self)\
          .get_instance_data(model, content, **kwargs)
        data['commenter_id'] = self.request.user.pk
        return data

class PlanCommentInstanceView (ModelInstanceMixin, views.InstanceModelView):
    resource = resources.PlanCommentResource
    permissions = [permissions.IsCommenterOrReadOnly]


class PlanSupportListView (views.ListOrCreateModelView):
    resource = resources.PlanSupportResource

    def get_instance_data(self, model, content, **kwargs):
        """Get the supporting user as the one that is logged in."""
        data = super(PlanSupportListView, self)\
          .get_instance_data(model, content, **kwargs)
        data['supporter_id'] = self.request.user.pk
        return data

    def post(self, request, *args, **kwargs):
        # Users should only be able to support a plan once, and this is enforced
        # by the ORM/DB.  Gracefully handle the integrity error.
        try:
            return super(PlanSupportListView, self).post(request, *args, **kwargs)
        except IntegrityError:
            raise ErrorResponse(status.HTTP_409_CONFLICT,
                                {'detail': ('User has already supported '
                                'that plan.')})

class PlanSupportInstanceView (ModelInstanceMixin, views.InstanceModelView):
    resource = resources.PlanSupportResource
    permissions = [permissions.IsSupporterOrReadOnly]


class PlanLinkListView (views.ListOrCreateModelView):
    resource = resources.PlanLinkResource

    
class PlanLinkInstanceView (ModelInstanceMixin, views.InstanceModelView):
    resource = resources.PlanLinkResource
    permissions = [permissions.IsPlanOwnerOrReadOnly]
