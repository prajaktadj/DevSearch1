from datetime import datetime
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Project,Review,Tag
from django.contrib import messages
from .forms import ProjectForm,ReviewForm
from django.contrib.auth.decorators import login_required
from .utils import searchProjects


# Create your views here.

#def projects(request):
    #return HttpResponse("This is going to list all the projects")

#def project(request,pk):
    #return HttpResponse('single project'+(pk))

#def projects(request):
    #return render(request,'index.html')

#def projects(request):
    #return render(request,'projects.html')

#def project(request,pk):
    #return render(request,'projs/single-project.html')

def projects(request):
    #return render(request,'main.html')
    return render(request,'projs/projects.html')

     #Pass parameter to the template of singleproject HTML
#def project(request,pk):
    #return render(request,'projs/single-project.html',{'primarykey':pk})

      #you can pass parameter like this also
def project(request,pk):
    context={'primarykey':pk,}
    return render(request,'projs/single-project.html',context)

    #if you wnt to add more variables to the parameter
def project(request,pk):
    context={'primarykey':pk,'number':10,}
    return render(request,'projs/single-project.html',context)    

     #pass default number into the project
def projects(request):
    context  = {'number':10}
    return render(request,'projs/projects.html',context)


#add list then display it from projects:

projectsList = [
    {
        'id' : '1',
        'title' : 'Ecommerce Website',
        'description' : 'Fully  functional ecommerce website'
    },
    {
        'id' : '2',
        'title' : 'Portfolio Website',
        'description' : 'A personal website to write articles and display work'
    },
    {
        'id' : '3',
        'title' : 'Social Network',
        'description' : 'An open source project built by the community'
    }
]

'''def projects(request):
    context  = {'proj_list' : projectsList,
                'number':10}
    return render(request,'projs/projects.html',context)'''

#get the project when you pass id as parameter:

'''def project(request,pk):
    proj_dict = None
    for p_dict in projectsList:
        if p_dict['id'] == pk:
           proj_dict = p_dict
    context = {'proj' : proj_dict,}
    return render(request,'projs/single-project.html',context)'''

#display 2 project when passing 2 ids as parameters

'''def project(request,pk,id2):
    proj_dict = None
    proj_dict2 = None
    for p_dict in projectsList:
        if p_dict['id'] == pk:
           proj_dict = p_dict
        if p_dict['id'] == id2:
           proj_dict2 = p_dict
    context = {'proj' : proj_dict,
               'proj2' : proj_dict2,}
    return render(request,'projs/single-project.html',context)  '''  

    #get the title as link

'''def projects(request):
    d_val = datetime.now()
    context  = {'proj_list' : projectsList,
                'number':10,
                'd_val':d_val}
    return render(request,'projs/projects.html',context)'''

'''def createproject(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form,
               }
    return render(request,'projs/create-project.html',context)'''

'''def projects(request):
    project_list = Project.objects.all()            #we get all the projects from DB
    context = {'projects': project_list}
    return render(request,'projs/projects.html',context)'''

def projects(request):
    project_list, search_query = searchProjects(request)
   #project_list = Project.objects.all()  
    context = {'projects': project_list,
               'search_query': search_query,
    }
    return render(request,'projs/projects.html',context)

def project(request,pk):
    proj = None
    proj = Project.objects.get(id=pk)
    review_form = ReviewForm()
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review =review_form.save(commit=False)
            review.project = proj
            review.owner = request.user.profile
            review.save()

            proj.getVoteCount
            
            messages.success(request,'Comment Added Successfully')
            return redirect('projects:project',pk=proj.id)
        else:
            messages.error(request,'error occured')

    context = {'proj' : proj,
               'review_form':review_form,
               
    }
    return render(request,'projs/single-project.html',context)

@login_required(login_url='users:login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            messages.success(request,'Project Created Successfully')
            return redirect('users:account')
    context = {'form' : form}
    return render(request,'projs/create-project.html',context)

@login_required(login_url='users:login')
def updateProject(request,pk):
    profile = request.user.profile
    proj = profile.project_set.get(id=pk)
    proj_form = ProjectForm(instance = proj)
    if request.method == 'POST':
        proj_form = ProjectForm(request.POST,request.FILES,instance = proj)
        if proj_form.is_valid():
            proj_form.save()
            messages.success(request,'Updated Successfully')
            return redirect('users:account')
        else:
            messages.error(request,'some error occured')
    context = {'proj_form':proj_form,}
    return render(request,'projs/update-project.html',context)

@login_required(login_url='users:login')
def deleteProject(request,pk):
    profile = request.user.profile
    proj = profile.project_set.get(id=pk)
    if request.method == 'POST':
        proj.delete()
        messages.success(request,'project deleted successfully')
        return redirect('users:account')
    context = {'object':proj}
    return render(request,'projs/delete-project.html',context)
