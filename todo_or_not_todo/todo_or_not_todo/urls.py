from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('requirements_tracker.urls')),  # This makes the application appear as a default app
    # Examples:
    # url(r'^$', 'todo_or_not_todo.views.home', name='home'),
    # url(r'^todo_or_not_todo/', include('todo_or_not_todo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^requirements_tracker/', include('requirements_tracker.urls')),
)
