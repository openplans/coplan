from djangorestframework import permissions
from djangorestframework import status
from djangorestframework.response import ErrorResponse
from . import models

class IsInstanceUserOrReadOnly (permissions.BasePermission):
    model = None
    """The Model class that the instance belongs to"""

    user_attr = None
    """The name of the user attribute"""
    
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


