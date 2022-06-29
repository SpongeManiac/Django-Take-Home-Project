# 'View' is the base implementation of all other views.
# It is very basic and functionality must be explicitly defined.
# 'TemplateView' is used for easily displaying a webpage based
# on a template.
from django.views.generic import View, TemplateView

# 'SingleTableView' is used to easily generate a table to represent
# models. It is from the 'django_tables2' package and not standard.
from django_tables2 import SingleTableView

# 'FormView' is used to easily create webpages from a form.
from django.views.generic.edit import FormView

# 'login' is used to easily log in a User.
# 'logout' is used to easily log out a User.
from django.contrib.auth import login, logout

# 'method_decorator' is used to decorate a specific function in a
# class without having to define it. It is used in combination with
# 'login_required' to restrict access to certain views when the user
# is not authenticated (logged in).
from django.utils.decorators import method_decorator

# 'login_required' is a decorator used to restrict access to logged in users.
# It is used in combination with 'method_decorator' to easily restrict
# class-based views without having to define and decorate a method.
from django.contrib.auth.decorators import login_required

# 'redirect' is used to return a 'HttpResponseRedirect' to redirect the user 
# to another view, relative url, or absolute url.
# 'render' is used to preprocess templates and generate an 'HttpResonse'.
from django.shortcuts import redirect, render

# Import the models used in the views.
from CRUD_example.models import (
    Customer,
    CustomerSoftware,
    Software,
)

# Import the forms used in the views.
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

# Import the tables used in the views.
from CRUD_example.tables import(
    CustomerTable,
    SoftwareTable,
    CustomerSoftwareTable,
)


# 'IndexView' is a 'TemplateView'.
# 'IndexView' displays the home/root page using a template.
class IndexView(TemplateView):
    # Set the template to be used
    template_name = 'index.html'

# 'RegisterView' is a 'FormView'.
# 'RegisterView' displays the registration page using a template
# and a form.
class RegisterView(FormView):
    # Set the template to be used
    template_name = 'register.html'
    # Set the form to be used with the template
    form_class = RegisterForm
    # The url to be navigated to when the form is successfully submitted
    # with no ValidationErrors.
    success_url = '/login'

    # 'form_valid' is executed when the form is successfully submitted
    # with no ValidationErrors.
    def form_valid(self, form):
        # Save the new User object using data submitted in the form
        form.save()
        # Redirect the user to the success_url (/login)
        return redirect(self.get_success_url())


# 'LoginView' is a 'FormView'.
# 'LoginView' displays the login page using a template and a form.
class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'
    
    # This view is slightly different from the previous, despite
    # them extending from the same class.
    # 'get' is the function that handles get requests to this view.
    # It is normally not defined as the base class already defines it.
    # However, this view needs to evaluate whether the request is from
    # an authenticated user.
    def get(self, request, *args, **kwargs):
        # Get the 'next' parameter from the url.
        # This parameter should be the url the user was trying to access
        # while logged out. If the value does not exist, simply use the 
        # success url instead.
        next = request.GET.get('next', self.success_url)
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Redirect the user since they are already authenticated.
            return redirect(next)
        else:
            # The user is not authenticated. Display the login page.
            return super(FormView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        # The form info is valid, attempt to authenticate the user with
        # credentials provided by the form.
        user  = form.auth()
        # Obtain the 'next' parameter from the url. Use the success url if
        # it is not present.
        next = self.request.POST.get('next', self.success_url)
        # Safeguard against an empty 'next' parameter.
        if next == '':
            next = self.success_url
        # Check if the user returned from authentication exists
        if user is not None:
            # User exists, meaning authentication succeeded. Login the User
            login(self.request, user)
            # Redirect to the next url
            return redirect(next)
        else:
            # User does not exist, meaning authentication failed
            # 'auth_failed' adds a 'ValidationError' to the form
            form.auth_failed()
            # Return the login page with the same form. This is so
            # the 'ValidationError' that was added will be displayed.
            return render(self.request, 'login.html', {'form':form})


# 'LogoutView' is a 'View'
# 'LogoutView' logs out the user.
class LogoutView(View):

    # This view is very simple, hence it extends 'View'.
    # Define what happens when a user sends a 'get' request to this view.
    def get(self, request, *args, **kwargs):
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Logout the user
            logout(request)
        # Regardless of whether the user is logged in or not,
        # redirect to the home page
        return redirect('index')


# 'method_decorator' is used to decorate a function without defining it.
# 'login_required' is the decorator to be used.
# 'name' is the name of the function to be decorated.
# This decorator prevents this view from being accessed by unauthenticated users.
@method_decorator(login_required, name='dispatch')

# 'CustomersView' is a 'SingleTableView'
# 'CustomersView' displays a table of 'Customer' objects.
class CustomersView(SingleTableView):
    # Set the model to be represented in the 'SingleTableView'
    model = Customer
    # Set the table that will display the model
    table_class = CustomerTable
    # Set the template that the table will be rendered in
    template_name = 'customers/customers.html'

@method_decorator(login_required, name='dispatch')
# 'NewCustomerView' is a 'FormView'
# 'NewCustomerView' displays a form for creating a new 'Customer' object.
class NewCustomerView(FormView):
    template_name = 'customers/editcustomer.html'
    form_class = NewCustomerForm
    success_url = '/customers'

    def form_valid(self, form):
        # Save the new 'Customer' object using the data submitted in the form
        form.save()
        # redirect to success_url
        return redirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
# 'EditCustomerView' is a 'FormView'
# 'EditCustomerView' displays a form to edit a 'Customer' object.
class EditCustomerView(FormView):
    template_name = 'customers/editcustomer.html'
    form_class = EditCustomerForm
    success_url = '/customers'

    # This view needs special functionality so the 'get' operator
    # is overriden, much like the 'LoginView'
    def get(self, request, *args, **kwargs):
        # Set 'id' variable from the url path. This is slightly different
        # from how you obtain a url parameter from the path.
        # url variables are added to 'kwargs', whereas url parameters are
        # added to the request object.
        # Safeguard against non-existing 'id' with a default value
        self.id = kwargs.get('id', -1)
        
        # Continue normally by calling the parent class's 'get' function.
        return super(FormView, self).get(request, *args, **kwargs)

    # The 'post' operator is also overriden to set the 'id' variable
    def post(self, request, *args, **kwargs):
        # Set 'id' variable from the url path.
        self.id = kwargs.get('id', -1)
        # Continue normally
        return super(FormView, self).post(request, *args, **kwargs)

    # 'get_form' is the function that creates and returns the form
    # to be used in the template.
    def get_form(self, form_class=None):
        # Check if the form_class exists
        if form_class is None:
            # Set the form class if it does not exist
            # 'get_form_class' gets the form class from the class's 'form_class' variable.
            # If 'form_class' is not set, a configuration error is thrown. 
            form_class = self.get_form_class()
        
        # Check if the 'id' exists
        if self.id != -1:
            # 'id' was not -1, meaning it is usable
            # Get the 'Customer' object with this id
            customer = Customer.objects.filter(id=self.id)
            # Check if a 'Customer' object with the given id exists
            if customer.exists():
                # 'Customer' object exists, return a form populated with the object through the 'instance' variable
                return form_class(instance=customer.first(), **self.get_form_kwargs())
        # Something didn't exist, create a form with an instance that has an invalid id. This ensures the template
        # will still display the correct text, but nothing will be updated if form is somehow posted.
        form = form_class(instance=Customer(id=-1), **self.get_form_kwargs())
        # Add empty cleaned_data and ValidationError
        form.no_instance()
        # Return form with error
        return form

    def form_valid(self, form):
        # Update 'Customer' object using data submitted in form
        form.save()
        return redirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
# 'DelCustomerView' is a 'View'
# 'DelCustomerView' deletes a 'Customer' object.
class DelCustomerView(View):
    
    def get(self, request, *args, **kwargs):
        self.id = kwargs.get('id', -1)
        if self.id != -1:
            customer = Customer.objects.filter(id=self.id)
            if customer.exists():
                customer.delete()
        return redirect('customers')

@method_decorator(login_required, name='dispatch')
# 'SoftwareView' is a 'SingleTableView'
# 'SoftwareView' displays a table of 'Software' objects.
class SoftwareView(SingleTableView):
    model = Software
    table_class = SoftwareTable
    template_name = 'software/software.html'

@method_decorator(login_required, name='dispatch')
# 'NewSoftwareView' is a 'FormView'
# 'NewSoftwareView' displays a form for creating a new 'Software' object.
class NewSoftwareView(FormView):
    template_name = 'software/editsoftware.html'
    form_class = NewSoftwareForm
    success_url = '/software'

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
# 'EditSoftwareView' is a 'FormView'
# 'EditSoftwareView' displays a form to edit a 'Software' object.
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
            software = Software.objects.filter(id=self.id)
            if software.exists():
                return form_class(instance=software.first(), **self.get_form_kwargs())
        form = form_class(instance=Software(id=-1), **self.get_form_kwargs())
        form.no_instance()
        return form

    def form_valid(self, form):
        form.save(self.id)
        return redirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
# 'DelSoftwareView' is a 'View'
# 'DelSoftwareView' deletes a 'Software' object.
class DelSoftwareView(View):

    def get(self, request, *args, **kwargs):
        self.id = kwargs.get('id', -1)
        if self.id != -1:
            software = Software.objects.filter(id=self.id)
            if software.exists():
                software.delete()
        return redirect('software')

@method_decorator(login_required, name='dispatch')
class CustomerSoftwareView(SingleTableView):
    # 'CustomerSoftwareView' is a 'SingleTableView'
    # 'CustomerSoftwareView' displays a table of 'CustomerSoftware' objects.
    model = CustomerSoftware
    table_class = CustomerSoftwareTable
    template_name = 'customersoftware/customersoftware.html'

@method_decorator(login_required, name='dispatch')
# 'NewCustomerSoftwareView' is a 'FormView'
# 'NewCustomerSoftwareView' displays a form for creating a new 'CustomerSoftware' object.
class NewCustomerSoftwareView(FormView):
    template_name = 'customersoftware/editcustomersoftware.html'
    form_class = NewCustomerSoftwareForm
    success_url = '/customersoftware'

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
# 'EditCustomerSoftwareView' is a 'FormView'
# 'EditCustomerSoftwareView' displays a form to edit a 'CustomerSoftware' object.
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
            customerSoftware = CustomerSoftware.objects.filter(id=self.id)
            if customerSoftware.exists():
                # Get the 'CustomerSoftware' object from QuerySet
                customerSoftware = customerSoftware.first()
                # Create the form with the 'CustomerSoftware' object
                form = form_class(instance=customerSoftware, **self.get_form_kwargs())
                # Set initial value for the 'customer' dropdown
                form.fields['customer'].initial = customerSoftware.cid
                # Set initial value for the 'software' dropdown
                form.fields['software'].initial = customerSoftware.sid
                # Return the form
                return form
        form = form_class(instance=CustomerSoftware(id=-1), **self.get_form_kwargs())
        form.no_instance()
        return form

    def form_valid(self, form):
        form.save(self.id)
        return redirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
# 'DelCustomerSoftwareView' is a 'View'
# 'DelCustomerSoftwareView' deletes a 'CustomerSoftware' object.
class DelCustomerSoftwareView(View):

    def get(self, request, *args, **kwargs):
        self.id = kwargs.get('id', -1)
        if self.id != -1:
            customerSoftware = CustomerSoftware.objects.filter(id=self.id)
            if customerSoftware.exists():
                customerSoftware.delete()
        return redirect('customersoftware')