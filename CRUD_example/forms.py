from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from CRUD_example.models import *
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
        
        #get vars
        e = cleaned_data.get('email', -1)
        p1 = cleaned_data.get('password1', -1)
        p2 = cleaned_data.get('password2', -1)

        if isinstance(e, str):
            if len(e) <= 3:
                self.add_error('email', ValidationError(_('Please enter a valid email.')))
        
        if isinstance(p1, str):
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

        e = cleaned_data.get('email', -1)
        p = cleaned_data.get('password', -1)

        if isinstance(e, str):
            if len(e) <= 3:
                self.add_error('email', ValidationError(_('Please enter a valid email.')))
        if isinstance(p, str):
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

        n = cleaned_data.get('name', -1)

        if isinstance(n, str):
            if len(n) < 3:
                self.add_error('name', ValidationError(_('Name must have at least 3 characters')))

        return cleaned_data
    
    def save(self):
        customer = Customer(name=self.cleaned_data['name'])
        customer.save()

class EditCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', )

    def clean(self):
        if self.instance.id == -1:
            for field in self.errors.keys():
                self.errors[field] = []
            return []

        cleaned_data = super().clean()

        n = cleaned_data.get('name', -1)

        if isinstance(n, str):
            if len(n) < 3:
                self.add_error('name', ValidationError(_('Name must have at least 3 characters.')))
        
        return cleaned_data

    def no_instance(self):
        self.cleaned_data = []
        for field in self.fields.keys():
            self.fields[field].disabled = True
        self.add_error(None, ValidationError(_('Not a valid id. Please edit a valid Customer.')))

    def save(self):
        # An id with no matches is possible, in which case nothing will happen.
        customer = Customer.objects.filter(id=self.instance.id)
        # Check if customer exists
        if customer.exists():
            # Customer exists, update it with values in form
            customer.update(name = self.cleaned_data['name'])

class NewSoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        fields = ('name', 'image')

    def clean(self):
        cleaned_data = super().clean()

        n = cleaned_data.get('name', -1)
        i = cleaned_data.get('image', -1)

        if isinstance(n, str):
            if len(n) <= 0:
                self.add_error('name', ValidationError(_('Name must have at least 1 character')))

        if isinstance(i, str):
            h = httplib2.Http()
            try:
                response, content = h.request(i, "HEAD", redirections=10)
                if response.status == 200:
                    type = response['content-type']
                    split_text = type.split('/')
                    print(split_text)
                    if split_text[0] == 'image':
                        if split_text[1] in VALID_IMAGE_TYPES:
                            cleaned_data['image'] = response['content-location']
                            print(cleaned_data['image'])
                            return cleaned_data
                        else:
                            self.add_error('image', ValidationError(_('Image is not of type PNG, JPG, or JPEG.')))
                    else:
                        self.add_error('image', ValidationError(_('URL is not an image. Expected \'image/(png, jpg, jpeg)\', got \''+type+'\' instead.')))
                else:
                    self.add_error('image', ValidationError(_('URL is not valid.')))
            except httplib2.ServerNotFoundError:
                self.add_error('image', ValidationError(_('URL is not valid.')))
            except httplib2.RedirectLimit:
                self.add_error('image', ValidationError(_('URL exceeded max redirects (10).')))
            except:
                self.add_error('image', ValidationError(_('URL is not valid.')))

        return cleaned_data
    
    def save(self):
        software = Software(name=self.cleaned_data['name'], image=self.cleaned_data['image'])
        software.save()

class EditSoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        fields = ('name', 'image')

    def clean(self):
        if self.instance.id == -1:
            for field in self.errors.keys():
                self.errors[field] = []
            return []

        cleaned_data = super().clean()

        n = cleaned_data.get('name', -1)
        i = cleaned_data.get('image', -1)

        if isinstance(n, str):
            if len(n) <= 0:
                self.add_error('name', ValidationError(_('Name must have at least 1 character.')))

        if isinstance(i, str):
            h = httplib2.Http()
            try:
                response, content = h.request(i, "HEAD", redirections=10)
                if response.status == 200:
                    type = response['content-type']
                    split_text = type.split('/')
                    if split_text[0] == 'image':
                        if split_text[1] in VALID_IMAGE_TYPES:
                            cleaned_data['image'] = response['content-location']
                            print(cleaned_data['image'])
                            return cleaned_data
                        else:
                            self.add_error('image', ValidationError(_('Image is not of type PNG, JPG, or JPEG.')))
                    else:
                        self.add_error('image', ValidationError(_('URL is not an image.')))
                else:
                    self.add_error('image', ValidationError(_('URL is not valid.')))
            except httplib2.ServerNotFoundError:
                self.add_error('image', ValidationError(_('URL is not valid.')))
            except httplib2.RedirectLimit:
                self.add_error('image', ValidationError(_('URL exceeded max redirects (10).')))
            except:
                self.add_error('image', ValidationError(_('URL is not valid.')))
        return cleaned_data

    def valid_image(self):
        self.clean()
        return self.image_valid

    def no_instance(self):
        self.cleaned_data = []
        for field in self.fields.keys():
            self.fields[field].disabled = True
        self.add_error(None, ValidationError(_('Not a valid id. Please edit a valid Software.')))

    def save(self):
        software = Software.objects.filter(id=self.instance.id)
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

        c = cleaned_data.get('customer', -1)
        s = cleaned_data.get('software', -1)

        if not isinstance(c, Customer):
            self.add_error('customer', ValidationError(_('Please choose a customer.')))
        if not isinstance(s, Software):
            self.add_error('software', ValidationError(_('Please choose a software.')))

        return cleaned_data
    
    def save(self):
        customerSoftware = CustomerSoftware(cid=self.cleaned_data['customer'], sid=self.cleaned_data['software'])
        customerSoftware.save()

    def update(self, id):
        customerSoftware = CustomerSoftware.objects.filter(id=id)
        if customerSoftware.exists():
            customerSoftware.update(cid=self.cleaned_data['customer'], sid=self.cleaned_data['software'])

class EditCustomerSoftwareForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())
    software = forms.ModelChoiceField(queryset=Software.objects.all())

    class Meta:
        model = CustomerSoftware
        fields = ('customer', 'software')
    
    def clean(self):
        if self.instance.id == -1:
            for field in self.errors.keys():
                self.errors[field] = []
            return []
        
        cleaned_data = super().clean()

        c = cleaned_data.get('customer', -1)
        s = cleaned_data.get('software', -1)

        if not isinstance(c, Customer):
            self.add_error('customer', ValidationError(_('Please choose a customer.')))
        if not isinstance(s, Software):
            self.add_error('software', ValidationError(_('Please choose a software.')))
        
        return cleaned_data

    def no_instance(self):
        self.cleaned_data = []
        for field in self.fields.keys():
            self.fields[field].disabled = True
        self.add_error(None, ValidationError(_('Not a valid id. Please edit a valid CustomerSoftware.')))

    def save(self):
        customerSoftware = CustomerSoftware.objects.filter(id=id)
        if customerSoftware.exists():
            customerSoftware.update(cid=self.cleaned_data['customer'], sid=self.cleaned_data['software'])