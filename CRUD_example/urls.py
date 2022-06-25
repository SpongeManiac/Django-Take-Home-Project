"""CRUD_example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.urls import include, path
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
    path('', IndexView.as_view(), name='index'),

    path('register/', RegisterView.as_view(), name='register'),

    path('login/', LoginView.as_view(), name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),

    path('customers/', CustomersView.as_view(), name='customers'),
    path('customers/create', NewCustomerView.as_view(), name='newcustomer'),
    path('customers/edit/<int:id>', EditCustomerView.as_view(), name='editcustomer'),
    path('customers/delete/<int:id>', DelCustomerView.as_view(), name='delcustomer'),

    path('software/', SoftwareView.as_view(), name='software'),
    path('software/create', NewSoftwareView.as_view(), name='newsoftware'),
    path('software/edit/<int:id>', EditSoftwareView.as_view(), name='editsoftware'),
    path('software/delete/<int:id>', DelSoftwareView.as_view(), name='delsoftware'),

    path('customersoftware/', CustomerSoftwareView.as_view(), name='customersoftware'),
    path('customersoftware/create', NewCustomerSoftwareView.as_view(), name='newcustomersoftware'),
    path('customersoftware/edit/<int:id>', EditCustomerSoftwareView.as_view(), name='editcustomersoftware'),
    path('customersoftware/delete/<int:id>', DelCustomerSoftwareView.as_view(), name='delcustomersoftware'),
]
