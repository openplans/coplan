from django import forms
from . import models

class PlanCommentForm (forms.ModelForm):
    """
    The form used to validate comments.  The plan and the commenter are 
    both implicit from the view.
    """
    class Meta:
        model = models.Comment
        exclude = ['plan', 'commenter']


class PlanLinkForm (forms.ModelForm):
    """
    The form used to validate links.  The plan is implicit from the view.
    """
    class Meta:
        model = models.Link
        exclude = ['plan']
