from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^project/', include('project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'', include('django.contrib.auth.urls')),

    url(r'^login-form/$', 'django.views.generic.simple.direct_to_template',
        {'template': 'login-form.html'}),
    url(r'', include('social_auth.urls')),

    url(r'^', include('coplan.urls')),
)
