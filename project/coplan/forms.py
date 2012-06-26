from django import forms
from . import models

class PlanCommentForm (forms.ModelForm):
    class Meta:
        model = models.Comment
        exclude = ['plan']
