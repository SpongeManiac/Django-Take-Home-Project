# 'forms' contains the different form types and form fields
# Forms are HTML forms that are used to submit data to the server
# Fields are the inputs that appear in a form
from xml.dom import ValidationErr
from django import forms

# 'authenticate' is used to check if user credentials are correct
from django.contrib.auth import authenticate

# 'gettext' is a function that converts a string to other languages
# It is imported as '_' for ease of use
from django.utils.translation import gettext as _

# 'ValidationError' creates visual form errors to communicate issues
# with form data/entries to the user.
from django.core.exceptions import ValidationError

# Import models to be used in the forms
from CRUD_example.models import (
    User,
    Login,
    Customer,
    Software,
    CustomerSoftware,
)

# 'httplib2' is an Http library used for making 'HEAD' requests and
# determining the Mime-Type of a url
import httplib2

# 'VALID_IMAGE_TYPES' is an array representing each valid image Mime-Type
VALID_IMAGE_TYPES = [
    'png',
    'jpeg',
    'jpg',
]

# 'validate_image' is used to validate that a url is an image
def validate_image(self, url, cleaned_data):
    # Create an Http instance
    h = httplib2.Http()
    # Encapsulate in try/catch to prevent serverside errors
    try:
        # Send a 'HEAD' request to the given url. It will follow redirects
        # until it reaches the specified max redirects
        response, content = h.request(url, "HEAD", redirections=10)
        # Check if the last response was 'OK' (200)
        if response.status == 200:
            # Get the content type (Mime-Type) of the response
            type = response['content-type']
            # Split the content type at the slash
            split_text = type.split('/')
            # Check if the content type is an image
            if split_text[0] == 'image':
                # Check if the image type is in 'VALID_IMAGE_TYPES'
                if split_text[1] in VALID_IMAGE_TYPES:
                    # Get the final url location of the image
                    cleaned_data['image'] = response['content-location']
                    # Return cleaned_data
                    return cleaned_data
                else:
                    # Image type is not supported, add an error
                    self.add_error('image', ValidationError(_('Image is not of type PNG, JPG, or JPEG.')))
            else:
                # Content type was not an image, add an error
                self.add_error('image', ValidationError(_('URL is not an image. Expected \'image/(png, jpg, jpeg)\', got \''+type+'\' instead.')))
        else:
            # Response was not 'OK', add an error
            self.add_error('image', ValidationError(_('URL is not valid.')))
    except httplib2.ServerNotFoundError:
        # Server could not be reached, add an error
        self.add_error('image', ValidationError(_('URL is not valid.')))
    except httplib2.RedirectLimit:
        # Max redirects has been reached, add an error
        self.add_error('image', ValidationError(_('URL exceeded max redirects (10).')))
    except:
        # A catch-all for any other unexpected errors
        self.add_error('image', ValidationError(_('URL is not valid.')))
    # Return cleaned_data
    return cleaned_data

# 'RegisterForm' is a 'Form'
# 'RegisterForm' is a form for creating new 'User' objects
# A 'ModelForm' is not used because custom fields and functionality are needed
class RegisterForm(forms.Form):
    # Create relevant fields to create a 'User' object
    email = forms.EmailField(required=True, max_length=512, label='Email')
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    def clean(self):
        # Clean the data like normal
        cleaned_data = super().clean()
        
        # Get cleaned variables
        e = cleaned_data.get('email', '')
        p1 = cleaned_data.get('password1', '')
        p2 = cleaned_data.get('password2', '')

        # Check if variable is a string
        if isinstance(e, str):
            # Check if email is at least 4 characters long
            if len(e) < 3:
                # Email is too small, add an error
                self.add_error('email', ValidationError(_('Please enter a valid email.')))
            
            # Check if user already exists
            user = User.objects.filter(email=self.cleaned_data['email'])
            if user.exists():
                # User with this email already exists, add an error
                self.add_error('email', ValidationError(_('User with this email already exists.')))
        else:
            # 'email' field is not a string, add error
            self.add_error('email', ValidationError(_('Email must be a string.')))
        
        # Check if password is a string
        if isinstance(p1, str):
            # Check if either password is less than 6 characters long
            if len(p1) < 6 or len(p2) < 6:
                self.add_error(None, ValidationError(_('Password must be at least 6 characters long.')))

            # Check if passwords match
            if not p1 == p2:
                self.add_error(None, ValidationError(_('Passwords do not match.')))
        else:
            # 'password' field is not a string, add error
            self.add_error('password', ValidationError(_('Password must be a string.')))

        # Return the cleaned_data
        return cleaned_data

    # 'save' will create a new user from the data provided to the form
    def save(self):
        # Create new user
        user = User.objects.create_user(email=self.cleaned_data['email'], password=self.cleaned_data['password1'])
        # Save new user
        user.save()
        # Return the new user in case it is needed
        return user

# 'LoginForm' is a 'Form'
# 'LoginForm' is a form for logging in
class LoginForm(forms.Form):
    # Define form fields
    email = forms.EmailField(required=True, max_length=512, label='Email')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')

    def clean(self):
        cleaned_data = super().clean()

        e = cleaned_data.get('email', '')
        p = cleaned_data.get('password', '')

        if isinstance(e, str):
            # Check if email is 
            if len(e) < 3:
                self.add_error('email', ValidationError(_('Please enter a valid email.')))
        else:
            # 'email' field is not a string, add an error
            self.add_error('email', ValidationError(_('Email must be a string.')))

        if isinstance(p, str):
            if len(p) < 6:
                self.add_error('password', ValidationError(_('Password must be at least 6 characters long.')))
        else:
            self.add_error('password', ValidationError(_('Password must be a string.')))
        
        return cleaned_data

    # 'auth' will return the results of 'authenticate' using the data provided to the form
    def auth(self):
        return authenticate(username=self.cleaned_data['email'], password=self.cleaned_data['password'])

    # 'auth_failed' will add a validation error to the form
    def auth_failed(self):
        self.add_error(None, ValidationError(_('Login credentials invalid.')))

# 'NewCustomerForm' is a 'ModelForm'
# 'NewCustomerForm' is a form for creating new 'Customer' objects
class NewCustomerForm(forms.ModelForm):
    # The 'Meta' class is how we define the structure of the form
    class Meta:
        # 'model' is the model to create a form out of
        model = Customer
        # 'fields' is a tuple of strings that defines which model
        # variables to turn into form input fields
        fields = ('name', )
    
    def clean(self):
        cleaned_data = super().clean()

        n = cleaned_data.get('name', '')

        if isinstance(n, str):
            if len(n) < 3:
                self.add_error('name', ValidationError(_('Name must have at least 3 characters.')))
        else:
            self.add_error('name', ValidationError(_('Name must be a string.')))

        return cleaned_data
    
    # 'save' creates a new 'Customer' object and saves it to the db
    def save(self):
        customer = Customer(name=self.cleaned_data['name'])
        customer.save()

# 'EditCustomerForm' is a 'ModelForm'
# 'EditCustomerForm' is a form for updating 'Customer' objects
class EditCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', )

    def clean(self):
        # Safeguard against non-existant ids
        # instance will have an 'id' of -1 if the object to edit did not exist
        if self.instance.id == -1:
            # remove validation errors from all fields
            for field in self.errors.keys():
                self.errors[field] = []
            # return empty cleaned_variables
            return []

        cleaned_data = super().clean()

        n = cleaned_data.get('name', '')

        if isinstance(n, str):
            if len(n) < 3:
                self.add_error('name', ValidationError(_('Name must have at least 3 characters.')))
        else:
            self.add_error('name', ValidationError(_('Name must be a string.')))

        return cleaned_data

    # 'no_instance' is called when the form is created with a non-existant id
    def no_instance(self):
        # Set cleaned_data to be empty
        self.cleaned_data = []
        # Disable all fields
        for field in self.fields.keys():
            self.fields[field].disabled = True
        # Add an error
        self.add_error(None, ValidationError(_('Not a valid id. Please edit a valid Customer.')))

    # 'save' updates a 'Customer' object with the data given to the form
    def save(self):
        # An id with no matches is possible, in which case nothing will happen.
        customer = Customer.objects.filter(id=self.instance.id)
        # Check if customer exists
        if customer.exists():
            # Customer exists, update it with values in form
            customer.update(name = self.cleaned_data['name'])

# 'NewSoftwareForm' is a 'ModelForm'
# 'NewSoftwareForm' is a form for creating a new 'Software' object
class NewSoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        fields = ('name', 'image')

    def clean(self):
        cleaned_data = super().clean()

        n = cleaned_data.get('name', '')
        i = cleaned_data.get('image', '')

        if isinstance(n, str):
            if len(n) < 1:
                self.add_error('name', ValidationError(_('Name must have at least 1 character.')))
        else:
            self.add_error('name', ValidationError(_('Name must be a string.')))

        if isinstance(i, str):
            # Ensure that image url is a valid image
            cleaned_data = validate_image(self, i, cleaned_data)
        else:
            self.add_error('image', ValidationError(_('Image must be a string.')))

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

        n = cleaned_data.get('name', '')
        i = cleaned_data.get('image', '')

        if isinstance(n, str):
            if len(n) < 1:
                self.add_error('name', ValidationError(_('Name must have at least 1 character.')))
        else:
            self.add_error('name', ValidationError(_('Name must be a string.')))

        if isinstance(i, str):
            cleaned_data = validate_image(self, i, cleaned_data)
        else:
            self.add_error('image', ValidationError(_('Image must be a string.')))

        return cleaned_data

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

        # Ensure that the 'customer' field is a 'Customer' object
        if not isinstance(c, Customer):
            self.add_error('customer', ValidationError(_('Please choose a customer.')))

        # Ensure that the 'software' field is a 'Software' object
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