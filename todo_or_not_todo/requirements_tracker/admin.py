from django.contrib import admin
from requirements_tracker.models import User, Project, Task

admin.site.register(Project)
admin.site.register(Task)