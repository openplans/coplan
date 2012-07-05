import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import models as auth_models
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
    planner = models.Planner.objects.get(pk=request.user.pk)
    context = RequestContext(request, {
        'planner': planner,
    })
    return render_to_response('plan_detail.html', context_instance=context)


def edit_plan(request, pk):
    plan = get_object_or_404(models.Plan, pk=pk)

    if request.user.is_authenticated():
        planner = models.Planner.objects.get(pk=request.user.pk)
    else:
        planner = models.Planner()
        
    context = RequestContext(request, {
        'planner': planner,
        'plan': plan,
        'plan_data': json.dumps(resources.PlanResource().serialize(plan),
                                cls=DateTimeAwareJSONEncoder)
    })
    return render_to_response('plan_detail.html', context_instance=context)

def user_profile(request, pk):
    owner = get_object_or_404(auth_models.User, pk=pk)
    context = RequestContext(request, {
        'owner': owner
    })
    return render_to_response('user_profile.html', context_instance=context)
