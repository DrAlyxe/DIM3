from django.shortcuts import render_to_response
from requirements_tracker.forms import UserForm, ProjectForm, TaskForm
from requirements_tracker.models import Project, Task
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.core.exceptions import MultipleObjectsReturned

#some helper functions
def decode_url(url):
    return url.replace('_', ' ')

def encode_url(name):
    return name.replace(' ', '_')

def get_project_tasks_collaborators(project_name):
    context_dict = {}
    try:
        project = Project.objects.get(title = project_name)
        tasks = Task.objects.filter(project = project.id)
        context_dict['tasks'] = tasks
        collaborators = project.collaborators.all()
        context_dict['collaborators'] = collaborators
    except Project.DoesNotExist, MultipleObjectsReturned:
        return render_to_response('requirements_tracker/project.html', {}, None)
    return context_dict

def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {}
    all_projects = []
    projects = Project.objects.all()
    for project in projects:
        all_projects += [{'project_name_url': encode_url(project.title), 'title': project.title}]
    context_dict['all_projects'] = all_projects
   

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('requirements_tracker/index.html', context_dict, context)

def register(request):
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        user_form = UserForm(data=request.POST)

        #if form is valid
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors

    # Not a HTTP POST, so we render our form using ModelForm instance.
    # This form will be blank, ready for user input.
    else:
        user_form = UserForm()

    return render_to_response(
        'requirements_tracker/register.html',
        {'user_form': user_form, 'registered': registered},
        context)

def user_login(request):
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/requirements_tracker/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('requirements_tracker/login.html', {}, context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/requirements_tracker/')


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def new_project(request):
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = ProjectForm()
    return render_to_response('requirements_tracker/newproject.html', {"form" : form}, context)

@login_required
def add_tasks(request, project_name_url):
    context = RequestContext(request)
    project_name = decode_url(project_name_url)
    context_dict = {}
    context_dict['project_name'] = project_name
    context_dict['project_name_url'] = project_name_url
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        form = TaskForm(request.POST)
        context_dict['form'] = form
        if form.is_valid():
            page = form.save(commit=False)
            try:
                proj = Project.objects.get(title = project_name)
                page.project = proj
                page.save()
                return HttpResponseRedirect('/requirements_tracker/project/'+project_name_url+'/')
            except Project.DoesNotExist, Project.MultipleObjectsReturned:
                #Wrong url means non existant or wrong project name so just redirect to index page
                return HttpResponseRedirect('/requirements_tracker/', context_dict, context)
        else:
            form.errors
    else:
        form = TaskForm()
        context_dict['form'] = form
    return render_to_response('requirements_tracker/addtasks.html', context_dict, context)
    
@login_required
def project(request, project_name_url):
    context = RequestContext(request)
    project_name = decode_url(project_name_url)
    context_dict = get_project_tasks_collaborators(project_name)
    context_dict['project_name_url'] = project_name_url
    context_dict['project_name'] = project_name
    return render_to_response('requirements_tracker/project.html', context_dict, context)

@login_required
def edit_project(request, project_name_url):
    context = RequestContext(request)
    project_name = decode_url(project_name_url)
    context_dict = get_project_tasks_collaborators(project_name)
    context_dict['project_name_url'] = project_name_url
    context_dict['project_name'] = project_name  
    try:
        project = Project.objects.get(title = project_name)
    except Project.DoesNotExist, Project.MultipleObjectsReturned:
        return HttpResponseRedirect('/requirements_tracker/', {}, context)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            page = form.save(commit=True)
            return HttpResponseRedirect('/requirements_tracker/project/'+page.title+'/',
                                        context_dict, context)
        else:
            print form.errors
    else:
        form = ProjectForm(instance = project)
    
    context_dict['form'] = form
    return render_to_response('requirements_tracker/edit_project.html', context_dict, context)

@login_required
def profile(request):
    context = RequestContext(request)
    projects = Project.objects.filter(collaborators=request.user.id)
    context_dict = {}
    user_projects = []
    for project in projects:
        user_projects += [{"title": project,"project_name_url": encode_url(str(project))}]
    context_dict['user_projects'] = user_projects
    context_dict['user'] = request.user
    return render_to_response('requirements_tracker/profile.html', context_dict, context)
    





