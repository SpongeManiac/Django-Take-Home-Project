from django import forms
from django.contrib.auth import authenticate, login
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from CRUD_example.models import *
from urllib.parse import urlparse
import httplib2

VALID_IMAGE_TYPES = [
    'png',
    'jpeg',
    'jpg',
]

class RegisterForm(forms.Form):
    email = forms.EmailField(required=True, max_length=512, label='Email')
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean(self):
        #clean the data
        cleaned_data = super().clean()
        
        #check if passwords match
        p1 = cleaned_data['password1']
        p2 = cleaned_data['password2']

        if len(p1) <= 5 or len(p2) <= 5:
            self.add_error(None, ValidationError(_('Password must be at least 6 characters long.')))

        #check if p1 == p2
        if not p1 == p2:
            self.add_error(None, ValidationError(_('Passwords do not match.')))
        
        return cleaned_data

    def save(self):
        user = User.objects.create_user(email=self.cleaned_data['email'], password=self.cleaned_data['password1'])
        user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(required=True, max_length=512, label='Email')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')

    class Meta:
        model = Login
        fields = ('email', 'password')

    def clean(self):
        cleaned_data = super().clean()

        e = cleaned_data['email']
        p = cleaned_data['password']

        if len(e) == 0:
            self.add_error('email', ValidationError(_('Must have email')))

        if len(p) <= 5:
            self.add_error('password', ValidationError(_('Password must be at least 6 characters long.')))

        return cleaned_data

    def auth(self):
        return authenticate(username=self.cleaned_data['email'], password=self.cleaned_data['password'])

    def auth_failed(self):
        self.add_error(None, ValidationError(_('Login credentials invalid.')))

class NewCustomerForm(forms.Form):
    name = forms.CharField(required=True, max_length=255)

    class Meta:
        model = Customer
        fields = ('name', )
    
    def clean(self):
        cleaned_data = super().clean()

        n = cleaned_data['name']
        if len(n) <= 0:
            self.add_error('name', ValidationError(_('Name must have at least 1 character')))

        return cleaned_data
    
    def save(self):
        customer = Customer(name=self.cleaned_data['name'])
        customer.save()

class EditCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', )

    def clean(self):
        cleaned_data = super().clean()

        n = cleaned_data['name']
        if len(n) <= 0:
            self.add_error('name', ValidationError(_('Name must have at least 1 character')))
        
        return cleaned_data

    def save(self, id):
        customer = Customer.objects.filter(pk=id)
        if customer.exists():
            customer.update(name = self.cleaned_data['name'])

class NewSoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        fields = ('name', 'image')

    def clean(self):
        cleaned_data = super().clean()

        n = cleaned_data['name']
        i = cleaned_data['image']

        if len(n) <= 0:
            self.add_error('name', ValidationError(_('Name must have at least 1 character')))

        return cleaned_data
    
    def save(self):
        software = Software(name=self.cleaned_data['name'], image=self.cleaned_data['image'])
        software.save()

class EditSoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        fields = ('name', 'image')

    def clean(self):
        cleaned_data = super().clean()

        n = cleaned_data['name']
        i = cleaned_data['image']

        if len(n) <= 0:
            self.add_error('name', ValidationError(_('Name must have at least 1 character')))

        h = httplib2.Http()
        try:
            response, cont = h.request(i, "HEAD", redirections=10)
            if response.status == 200:
                type = response['content-type']
                split_text = type.split('/')
                if split_text[0] == 'image':
                    if split_text[1] in VALID_IMAGE_TYPES:
                        self.image_valid = True
                        cleaned_data['image'] = response['content-location']
                        print(cleaned_data['image'])
                        return cleaned_data
                    else:
                        self.add_error('image', ValidationError(_('Image is not of type PNG, JPG, or JPEG')))
                else:
                    self.add_error('image', ValidationError(_('URL is not an image.')))
            else:
                self.add_error('image', ValidationError(_('URL is not valid.')))
        except httplib2.ServerNotFoundError:
            self.add_error('image', ValidationError(_('URL is not valid.')))
        except httplib2.RedirectLimit:
            self.add_error('image', ValidationError(_('URL is not valid.')))
        self.image_valid = False
        return cleaned_data

    def valid_image(self):
        self.clean()
        return self.image_valid

    def save(self, id):
        software = Software.objects.filter(pk=id)
        if software.exists():
            software.update(name = self.cleaned_data['name'], image=self.cleaned_data['image'])

class NewCustomerSoftwareForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())
    software = forms.ModelChoiceField(queryset=Software.objects.all())

    class Meta:
        model = CustomerSoftware
        fields = ('customer', 'software')
    
    def clean(self):
        cleaned_data = super().clean()

        c = cleaned_data['customer']
        s = cleaned_data['software']

        if not c:
            self.add_error('customer', ValidationError(_('Please choose a customer.')))
        if not s:
            self.add_error('software', ValidationError(_('Please choose a software.')))

        return cleaned_data
    
    def save(self):
        customerSoftware = CustomerSoftware(cid=self.cleaned_data['customer'], sid=self.cleaned_data['software'])
        customerSoftware.save()

    def update(self, id):
        customerSoftware = CustomerSoftware.objects.filter(pk=id)
        if customerSoftware.exists():
            customerSoftware.update(cid=self.cleaned_data['customer'], sid=self.cleaned_data['software'])

class EditCustomerSoftwareForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())
    software = forms.ModelChoiceField(queryset=Software.objects.all())

    class Meta:
        model = CustomerSoftware
        fields = ('customer', 'software')
    
    def clean(self):
        cleaned_data = super().clean()

        c = cleaned_data['customer']
        s = cleaned_data['software']

        if not c:
            self.add_error('customer', ValidationError(_('Please choose a customer.')))
        if not s:
            self.add_error('software', ValidationError(_('Please choose a software.')))
        
        return cleaned_data

    def save(self, id):
        customerSoftware = CustomerSoftware.objects.filter(pk=id)
        if customerSoftware.exists():
            customerSoftware.update(cid=self.cleaned_data['customer'], sid=self.cleaned_data['software'])