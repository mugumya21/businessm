from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import  render
from  django.urls import reverse




# Create your views here.


#tasks =["foo", "books", "shoes"]

#a class that has the form and the form fields ie char or interger
class NewTaskForm(forms.Form):
    task= forms.CharField(label="New Task" , min_length=2, max_length=5)
    #priority=forms.IntegerField(label="priority", min_value=1, max_value=5)

    
def index(request):
    #use sessions to see if the use has just open the page ,he has been the one , if not , we will give him index.html empty for him to also add his tasks
    if "tasks" not in request.session:
        request.session["tasks"] = [] #session gives you an empty idex.html ie session is a big dictionary contain data 
    
    return render(request , "tasks/index.html" ,{
        "tasks":request.session["tasks"]  #here the session starts to capture the data.
    })
    
    
    
    
def add(request):
    # 1st: for the request post, verify
    if request.method == "POST":
        form =NewTaskForm(request.POST) #geting the data submited and puting it in the newTaskForm
        
        
        # 2nd: verifying the data
        if form.is_valid():
            #save in variable called task
            task = form.cleaned_data["task"] #give me all the data that the user has submited ie from  task= forms.CharField(label="New Task")
           # tasks.append(task) ; if you have tasks =["foo", "books", "shoes"]
           
            request.session["tasks"] +=[task] #add the task added before redirecting the use to the index.html
            
            #redirect him to the task or the index.html after submitting the work, ie reverse is for the url
            return HttpResponseRedirect(reverse("tasks:index")) #the index will be having his previous content
        else:
            #return an existing form
            return render(request, "tasks/add.html" ,{
                "form":form #with there the errors to be  corrected
            })
            
         
        
        #is the user has just open the form or after submitting , we are going to just render him the empty form

    return render(request, "tasks/add.html", {
             # get the template form and assign to class NewTaskForm
        "form":NewTaskForm()
    })
        

