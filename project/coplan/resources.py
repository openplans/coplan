from django.core.urlresolvers import reverse
from djangorestframework import resources
from . import forms
from . import models


def simple_user(planner):
    """Return a minimal representation of an auth.User"""
    return {
        'id': planner.pk,
        'name': planner.username,
        'profile_url': reverse('user_profile', args=(planner.pk,)),
        'avatar_url': planner.avatar_url,
    }

class PlanCommentResource (resources.ModelResource):
    model = models.Comment
    form = forms.PlanCommentForm
    exclude = ['plan']

    def commenter(self, comment):
        return simple_user(comment.commenter)


class PlanLinkResource (resources.ModelResource):
    model = models.Link
    form = forms.PlanLinkForm
    exclude = ['plan']

    
class PlanSupportResource (resources.ModelResource):
    model = models.Support
    form = forms.PlanSupportForm
    exclude = ['plan']

    def supporter(self, support):
        return simple_user(support.supporter)
    
    
class PlanResource (resources.ModelResource):
    model = models.Plan

    # By default, id is excluded.  Override exclude to be empty.
    exclude = ['supporters']
    include = [('comments', PlanCommentResource),
               ('links', PlanLinkResource),
               ('support', PlanSupportResource),
               ]

    def owner(self, plan):
        return plan.owner.pk

