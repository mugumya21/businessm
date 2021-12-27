from django.forms.models import inlineformset_factory
from django.shortcuts import redirect, render

from .decorators import admin_only, allowed_users, unauthenticated_user
from .models import *
from .forms import CreateUserForm, customerForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .filters import OrderFilter
from .forms import OrderForm
from django.contrib.auth.models import Group


# Create your views here.

def index(request):
    return render(request, "accounts/index.html")


@unauthenticated_user
def loginPage(request):
    #if the user is logged in to the dashboard, redirect him to the home page if he wants to access the login page
    #if request.user.is_authenticated:
       # return redirect('index')
   # else:
        if request.method=="POST":          
            username = request.POST.get("username") 
            password = request.POST.get('password')
            user =authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request,"Username or Password is incorrect")
                return render(request, "accounts/login.html")
        return render(request, "accounts/login.html")

  
@unauthenticated_user    
def register(request):
    #if request.user.is_authenticated:
       # return redirect('index')
    #else:
        form =CreateUserForm()
        if request.method== "POST":
                form =CreateUserForm(request.POST)
                if form.is_valid():
                   user= form.save()
                   username =form.cleaned_data.get("username") #get the name
                   
                   group = Group.objects.get(name='customer') 
                   user.groups.add(group)  #add it in the customer group
                   messages.success(request, "The account has beeen created for "+ username)
                   return redirect('login')

            
        context ={"form":form}
        return render(request, "accounts/register.html", context)
        


def logoutUser(request):
	logout(request)
	return redirect('login')






@login_required(login_url='login')
@admin_only
def dashboard(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'delivered':delivered,
	'pending':pending }

	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    #grab all the customer orders ie he have a relastionship btn user and the customer
    orders =request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()


    context = {'orders':orders, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request, "accounts/user.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()

	return render(request, 'accounts/products.html', {'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs 

	context = {'customer':customer, 'orders':orders, 'order_count':order_count,
	'myFilter':myFilter}
	return render(request, 'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('dashboard')

	context = {'form':formset}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('dashboard')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('dashboard')

	context = {'item':order}
	return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = customerForm(instance=customer)
    
    if request.method == 'POST':
        form = customerForm(request.POST , request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    
    context ={'form': form}
    return render(request, 'accounts/account_settings.html', context)