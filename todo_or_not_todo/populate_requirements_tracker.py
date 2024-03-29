import os

def populate():
    user1 = add_user(username = "user1", 
                     email = "fname1", 
                     password = "sname1")
    user2 = add_user(username = "user2", 
                     email = "fname2", 
                     password = "sname2")
    user3 = add_user(username = "user3", 
                     email = "fname3", 
                     password = "sname3")
    
    project1 = add_project(title = "project1", 
                           collaborators = [user1, user2])
    project2 = add_project(title = "project2", 
                           collaborators = [user2, user3])
    project3 = add_project(title = "project3")
    
    
    task1 = add_task(title = "task1", 
                     description = "description1", 
                     priority = 4, 
                     project = project1)
    
    task2 = add_task(title = "task2", 
                     description = "description2", 
                     priority = 1, 
                     project = project1)
    task3 = add_task(title = "task3", 
                     description = "description3", 
                     priority = 5, 
                     project = project3)
    task4 = add_task(title = "task4", 
                     description = "description4", 
                     priority = 4, 
                     project = project3)

    # Print out what we have added to the user.
    for u in User.objects.all():
        print u
    for p in Project.objects.all():
        s = str(p) + " -> "
        for u in p.collaborators.all():
            s += str(u) + " "
        print s
    for t in Task.objects.all():
        s = str(t) + " -> " + str(t.project)
        print s
    

def add_user(username, email, password):
    u = User.objects.get_or_create(username = username, email = email, password = password)[0]
    return u

def add_project(title, collaborators = []):
    p = Project.objects.get_or_create(title = title)[0]
    for user in collaborators:
        p.collaborators.add(user)
    return p

def add_task(title, description, project, priority = 0):
    t = Task.objects.get_or_create(title = title, description = description, priority = priority, project = project)[0]
    return t
    

# Start execution here!
if __name__ == '__main__':
    print "Starting Requirements Tracker population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_or_not_todo.settings')
    from requirements_tracker.models import Project, Task
    from django.contrib.auth.models import User
    populate()