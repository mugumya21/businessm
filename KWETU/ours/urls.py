from django.urls import path
from . import views


urlpatterns = [
	path('register/', views.register, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path("dashboard/",views.dashboard, name="dashboard"),
    path('', views.index, name="index"),
    path('products/', views.products, name='products'),
    path('customer/<str:pk_test>/', views.customer, name="customer"),
    path('user/', views.userPage, name="user-page"),
     path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
     path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    path('account/', views.accountSettings, name='account'),
]