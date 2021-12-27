from django.http import HttpResponse
from django.shortcuts import redirect


#view_func is the longin or register function
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        
        #text from the login function because we dont want to repeat it always on simillar pages, eg register
        if request.user.is_authenticated:
            return redirect('index')
        else: #calling the original func ie login or register
            return view_func(request, *args, **kwargs)
    return wrapper_func



def allowed_users(allowed_roles = []):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs ):
            
            group = None
            if request.user.groups.all():
                group = request.user.groups.all()[0].name
                
            if group in allowed_roles:
                return view_func(request, *args , **kwargs)
            else:
                return HttpResponse("You are not auntholised to access this page")
        return wrapper_func
    return decorator
                
                
def admin_only(view_func):
    def wrapper_function(request , *args, **kwargs):
        group = None
        if request.user.groups.all():
            group = request.user.groups.all()[0].name
            
        if group == 'customer':
            return redirect('user-page') #we use the name='user-page' from urls.py
        
        if group =='admin':
            return view_func(request , *args , **kwargs)
        
    return wrapper_function
                
        