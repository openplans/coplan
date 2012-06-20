from django.shortcuts import render_to_response
from django.template import RequestContext

def homepage(request):
    context = RequestContext(request, {})
    return render_to_response('index.html', context=context)


def new_plan(request):
    context = RequestContext(request, {
        })
    return render_to_response('plan_detail.html', context=context)
