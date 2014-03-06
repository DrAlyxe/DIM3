from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    # Auto-generated primary key as described here: 
    # https://docs.djangoproject.com/en/dev/topics/db/models/#id1 
    title = models.CharField(max_length=128)
    collaborators = models.ManyToManyField(User) 
    # Other fields may also be included

    def __unicode__(self):
        return self.title

class Task(models.Model):
    # Auto-generated primary key as described here: 
    # https://docs.djangoproject.com/en/dev/topics/db/models/#id1 
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    priority = models.PositiveSmallIntegerField()
    project = models.ForeignKey(Project)
    due_date = models.CharField(max_length=16)
    # Further fields added here
    
    def __unicode__(self):
        return self.title