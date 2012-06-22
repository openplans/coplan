import json
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from . import models
from . import resources

def homepage(request):
    context = RequestContext(request, {})
    return render_to_response('index.html', context_instance=context)

@login_required
def new_plan(request):
    context = RequestContext(request, {
        })
    return render_to_response('plan_detail.html', context_instance=context)


def edit_plan(request, pk):
    plan = get_object_or_404(models.Plan, pk=pk)
    context = RequestContext(request, {
        'plan': plan,
        'plan_data': json.dumps(resources.PlanResource().serialize(plan),
                                cls=DateTimeAwareJSONEncoder)
    })
    return render_to_response('plan_detail.html', context_instance=context)
