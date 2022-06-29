# We are not using django admin to manage our models
#from django.contrib import admin

#path is used to route the web app
from django.urls import path

# Import the views the app will use.
# I did not use 'import *' so that I can see which views I have implemented.
# This helps me stay organized while working.
from CRUD_example.views import (
    IndexView,
    RegisterView,
    LoginView,
    LogoutView,
    CustomersView,
    NewCustomerView,
    EditCustomerView,
    DelCustomerView,
    SoftwareView,
    NewSoftwareView,
    EditSoftwareView,
    DelSoftwareView,
    CustomerSoftwareView,
    NewCustomerSoftwareView,
    EditCustomerSoftwareView,
    DelCustomerSoftwareView,
)

urlpatterns = [
    #home/index page
    path('', IndexView.as_view(), name='index'),

    #authentication pages

    #registration page
    path('register/', RegisterView.as_view(), name='register'),
    #login page
    path('login/', LoginView.as_view(), name='login'),
    #logout view
    path('logout/', LogoutView.as_view(), name='logout'),
    
    #customer model pages

    #customer table page
    path('customers/', CustomersView.as_view(), name='customers'),
    #create customer page
    path('customers/create', NewCustomerView.as_view(), name='newcustomer'),
    #update customer page
    path('customers/edit/<int:id>', EditCustomerView.as_view(), name='editcustomer'),
    #delete customer view
    path('customers/delete/<int:id>', DelCustomerView.as_view(), name='delcustomer'),

    #software model pages

    #software table page
    path('software/', SoftwareView.as_view(), name='software'),
    #create software page
    path('software/create', NewSoftwareView.as_view(), name='newsoftware'),
    #update software page
    path('software/edit/<int:id>', EditSoftwareView.as_view(), name='editsoftware'),
    #delete software view
    path('software/delete/<int:id>', DelSoftwareView.as_view(), name='delsoftware'),

    #customer - software relation model pages

    #customer - software relation table page
    path('customersoftware/', CustomerSoftwareView.as_view(), name='customersoftware'),
    #create customer - software relation page
    path('customersoftware/create', NewCustomerSoftwareView.as_view(), name='newcustomersoftware'),
    #update customer - software relation page
    path('customersoftware/edit/<int:id>', EditCustomerSoftwareView.as_view(), name='editcustomersoftware'),
    #delete customer - software relation view
    path('customersoftware/delete/<int:id>', DelCustomerSoftwareView.as_view(), name='delcustomersoftware'),
]
