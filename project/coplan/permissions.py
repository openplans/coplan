from djangorestframework import permissions
from djangorestframework import status
from djangorestframework.response import ErrorResponse
from . import models

class IsInstanceUserOrReadOnly (permissions.BasePermission):
    model = None
    """The Model class that the instance belongs to"""

    user_attr = None
    """The name of the user attribute to get from self.get_instance().
    If it's a tuple, we do a chain of getattrs
    and the user is the last object returned.
    """

    def check_permission(self, user):
        view = self.view
        if view.method in ('GET', 'HEAD'):
            return
        try:
            inst = view.get_instance()

            if isinstance(self.user_attr, basestring):
                names = [self.user_attr]
            else:
                names = self.user_attr
            assert names, "user attr not specified"
            for name in names:
                inst = getattr(inst, name)
                
            if inst != user:
                raise ErrorResponse(
                    status.HTTP_403_FORBIDDEN,
                    {'detail': ('Only the {0} of a {1} may make '
                    'modifications.').format(' '.join(self.user_attr),
                                             self.model._meta.verbose_name)})

        except self.model.DoesNotExist:
            raise ErrorResponse(status.HTTP_404_NOT_FOUND)


class IsOwnerOrReadOnly (IsInstanceUserOrReadOnly):
    model = models.Plan
    user_attr = 'owner'

class IsPlanOwnerOrReadOnly (IsInstanceUserOrReadOnly):
    model = models.Link
    user_attr = ('plan', 'owner')
    

class IsCommenterOrReadOnly (IsInstanceUserOrReadOnly):
    model = models.Comment
    user_attr = 'commenter'

    
class IsSupporterOrReadOnly (IsInstanceUserOrReadOnly):
    model = models.Support
    user_attr = 'supporter'


