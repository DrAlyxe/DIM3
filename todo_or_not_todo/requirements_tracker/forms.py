from django import forms
from requirements_tracker.models import User, Project, Task

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')
        
class ProjectForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the project title.")

    # An inline class to provide additional information on the form.
    class Meta:
        model = Project
        fields = ('title', 'collaborators')

class TaskForm(forms.ModelForm):
    PRIORITY_CHOICES = (
                        ('1', 'Must have'),
                        ('2', 'Should have'),
                        ('3', 'Could have'),
                        ('4', 'Won\'t have')
                        )
    title = forms.CharField(max_length=128, help_text="Please enter the task title:")
    description = forms.CharField(max_length=512, help_text="Please enter the task description:")
    priority = forms.ChoiceField(choices = PRIORITY_CHOICES, help_text="Please choose priority for the task:")
    due_date = forms.DateField(help_text="Please select due date:")
    
    class Meta:
        model = Task
        
        fields = ('title', 'description', 'priority', 'due_date')
