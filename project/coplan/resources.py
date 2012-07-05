from django.core.urlresolvers import reverse
from djangorestframework import resources
from . import forms
from . import models


class PlanCommentResource (resources.ModelResource):
    model = models.Comment
    form = forms.PlanCommentForm
    exclude = ['plan']

    def commenter(self, comment):
        return {'id': comment.commenter.pk,
                'name': comment.commenter.username,
                'profile_url': reverse('user_profile', 
                                       args=(comment.commenter.pk,)),
                }


class PlanResource (resources.ModelResource):
    model = models.Plan

    # By default, id is excluded.  Override exclude to be empty.
    exclude = []
    include = [('comments', PlanCommentResource)]

    def owner(self, plan):
        return plan.owner.pk
