from django.conf.urls import patterns, url
from requirements_tracker import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^register/', views.register, name='register'),
        url(r'^login/', views.user_login, name='login'),
        url(r'^logout/', views.user_logout, name='logout'),
        url(r'^new_project/', views.new_project, name='new_project'),
        url(r'^project/(?P<project_name_url>\w+)/$', views.project, name='project'),
        url(r'^project/(?P<project_name_url>\w+)/add_task/$', views.add_tasks, name="add task"),
        url(r'^project/(?P<project_name_url>\w+)/edit/$', views.edit_project, name="edit project"),
		url(r'^profile/', views.profile, name='profile'),
		#url(r'^my_tasks/', views.my_tasks, name='my_tasks'),
)