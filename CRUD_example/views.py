
from urllib.request import HTTPRedirectHandler
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, View
from django_tables2 import SingleTableView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from CRUD_example.models import (
    Customer,
    CustomerSoftware,
    Software,

)

from CRUD_example.forms import (
    EditSoftwareForm,
    RegisterForm,
    LoginForm,
    NewCustomerForm,
    EditCustomerForm,
    NewSoftwareForm,
    EditSoftwareForm,
    NewCustomerSoftwareForm,
    EditCustomerSoftwareForm,
)

from CRUD_example.tables import(
    CustomerTable,
    SoftwareTable,
    CustomerSoftwareTable,
)

class IndexView(TemplateView):
    template_name = 'index.html'

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/login'

    def form_valid(self, form):
        #default implimentation redirects to success_url
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('software')
        else:
            return super(FormView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        user  = form.auth()
        next = self.request.POST.get('next', self.success_url)
        if next == '':
            next = self.success_url
        if user is not None:
            login(self.request, user)
            print(self.request.POST)
            return redirect(next)
        else:
            form.auth_failed()
            return render(self.request, 'login.html', {'form':form})


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return redirect('index')

@method_decorator(login_required, name='dispatch')
class CustomersView(SingleTableView):
    model = Customer
    table_class = CustomerTable
    template_name = 'customers/customers.html'

@method_decorator(login_required, name='dispatch')
class NewCustomerView(FormView):
    template_name = 'customers/editcustomer.html'
    form_class = NewCustomerForm
    success_url = '/customers'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
class EditCustomerView(FormView):
    template_name = 'customers/editcustomer.html'
    form_class = EditCustomerForm
    success_url = '/customers'

    def get(self, request, *args, **kwargs):
        self.id = kwargs.get('id', -1)
        return super(FormView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.id = kwargs.get('id', -1)
        return super(FormView, self).post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        
        if self.id != -1:
            customer = Customer.objects.filter(pk=self.id)
            if customer.exists():
                return form_class(instance=customer.first(), **self.get_form_kwargs())
        return super().get_form(form_class)

    def form_valid(self, form):
        form.save(self.id)
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
class DelCustomerView(View):
    
    def get(self, request, *args, **kwargs):
        self.id = kwargs.get('id', -1)
        if self.id != -1:
            customer = Customer.objects.filter(pk=self.id)
            if customer.exists():
                customer.delete()
        return redirect('customers')


@method_decorator(login_required, name='dispatch')
class SoftwareView(SingleTableView):
    model = Software
    table_class = SoftwareTable
    template_name = 'software/software.html'

@method_decorator(login_required, name='dispatch')
class NewSoftwareView(FormView):
    template_name = 'software/editsoftware.html'
    form_class = NewSoftwareForm
    success_url = '/software'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
class EditSoftwareView(FormView):
    template_name = 'software/editsoftware.html'
    form_class = EditSoftwareForm
    success_url = '/software'

    def get(self, request, *args, **kwargs):
        self.id = kwargs.get('id', -1)
        return super(FormView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.id = kwargs.get('id', -1)
        return super(FormView, self).post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        
        if self.id != -1:
            software = Software.objects.filter(pk=self.id)
            if software.exists():
                return form_class(instance=software.first(), **self.get_form_kwargs())
        return super().get_form(form_class)

    def form_valid(self, form):
        form.save(self.id)
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
class DelSoftwareView(View):

    def get(self, request, *args, **kwargs):
        self.id = kwargs.get('id', -1)
        if self.id != -1:
            software = Software.objects.filter(pk=self.id)
            if software.exists():
                software.delete()
        return redirect('software')

@method_decorator(login_required, name='dispatch')
class CustomerSoftwareView(SingleTableView):
    model = CustomerSoftware
    table_class = CustomerSoftwareTable
    template_name = 'customersoftware/customersoftware.html'

@method_decorator(login_required, name='dispatch')
class NewCustomerSoftwareView(FormView):
    template_name = 'customersoftware/editcustomersoftware.html'
    form_class = NewCustomerSoftwareForm
    success_url = '/customersoftware'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
class EditCustomerSoftwareView(FormView):
    template_name = 'customersoftware/editcustomersoftware.html'
    form_class = EditCustomerSoftwareForm
    success_url = '/customersoftware'

    def get(self, request, *args, **kwargs):
        self.id = kwargs.get('id', -1)
        return super(FormView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.id = kwargs.get('id', -1)
        return super(FormView, self).post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        
        if self.id != -1:
            customerSoftware = CustomerSoftware.objects.filter(pk=self.id)
            if customerSoftware.exists():
                customerSoftware = customerSoftware.first()
                form = form_class(instance=customerSoftware, **self.get_form_kwargs())
                form.fields['customer'].initial = customerSoftware.cid
                form.fields['software'].initial = customerSoftware.sid
                return form
        return super().get_form(form_class)

    def form_valid(self, form):
        form.save(self.id)
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
class DelCustomerSoftwareView(View):

    def get(self, request, *args, **kwargs):
        self.id = kwargs.get('id', -1)
        if self.id != -1:
            customerSoftware = CustomerSoftware.objects.filter(pk=self.id)
            if customerSoftware.exists():
                customerSoftware.delete()
        return redirect('software')