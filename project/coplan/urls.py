from django.conf.urls import patterns, url, include
from . import api
from . import views

urlpatterns = patterns(
    'coplan',

    url(r'^$', views.homepage, name='home'),
    url(r'^plans/$', views.new_plan, name='new_plan'),
    url(r'^plans/(?P<pk>\d+)/$', views.edit_plan, name='edit_plan'),
    url(r'^users/(?P<pk>\d+)/profile/$', views.user_profile, name='user_profile'),

    url(r'^api/', 
        include('djangorestframework.urls', namespace='djangorestframework')),
    url('^api/v1/plans/$', 
        api.PlanListView.as_view(), name='plan_list'),
    url('^api/v1/plans/(?P<pk>\d+)/$', 
        api.PlanInstanceView.as_view(), name='plan_instance'),
    url('^api/v1/plans/(?P<plan_id>\d+)/comments/$', 
        api.PlanCommentListView.as_view(), name='plan_comment_list'),
    url('^api/v1/plans/(?P<plan_id>\d+)/comments/(?P<pk>\d+)/$', 
        api.PlanCommentInstanceView.as_view(), name='plan_comment_instance'),
    url('^api/v1/plans/(?P<plan_id>\d+)/links/$', 
        api.PlanLinkListView.as_view(), name='plan_link_list'),
    url('^api/v1/plans/(?P<plan_id>\d+)/links/(?P<pk>\d+)/$', 
        api.PlanLinkInstanceView.as_view(), name='plan_link_instance'),
    url('^api/v1/plans/(?P<plan_id>\d+)/support/$', 
        api.PlanSupportListView.as_view(), name='plan_support_list'),
    url('^api/v1/plans/(?P<plan_id>\d+)/support/(?P<pk>\d+)/$', 
        api.PlanSupportInstanceView.as_view(), name='plan_support_instance'),
        
)
