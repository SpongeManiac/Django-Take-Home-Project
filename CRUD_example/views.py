
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from CRUD_example.forms import (
    RegisterForm,
    LoginForm,

)

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/login'

    def form_valid(self, form):
        #default implimentation redirects to success_url
        form.save()
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/software'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('software')
        else:
            return super(FormView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        user  = form.auth()
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.auth_failed()
            return render(self.request, 'login.html', {'form':form})


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return redirect('login')


@method_decorator(login_required, name='dispatch')
class SoftwareView(TemplateView):
    template_name = 'software.html'

@method_decorator(login_required, name='dispatch')
class CustomersView(TemplateView):
    template_name = 'customers.html'

@method_decorator(login_required, name='dispatch')
class CustomerSoftwareView(TemplateView):
    template_name = 'customersoftware.html'