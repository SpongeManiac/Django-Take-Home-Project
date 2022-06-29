# 'django_tables2' is a library for creating tables easily
# 'tables' contains all of the table types and table columns to be used
import django_tables2 as tables

# Import all models to be used in the tables
from CRUD_example.models import(
    Customer,
    Software,
    CustomerSoftware,
)

# 'CustomerTable' is a 'Table'
# 'CustomerTable' displays 'Customer' objects as a table
class CustomerTable(tables.Table):
    # Define a 'TemplateColumn' to create a column that uses a template for its cell
    # 'edit' is a column for editing or deleting each entry
    edit = tables.TemplateColumn(template_name = "customers/customerButtons.html")

    # The 'Meta' class is used to define the data the table will display
    class Meta:
        # 'model' is the model to be used
        model = Customer
        # 'template_name' is the template to use for the table
        template_name = 'django_tables2/bootstrap.html'
        # 'fields' are the columns to be displayed
        fields = ('name', 'edit')

# 'SoftwareTable' is a 'Table'
# 'SoftwareTable' displays 'Software' objects as a table
class SoftwareTable(tables.Table):
    # An additional column is needed to display the 'Software' object's corresponding logo
    logo = tables.TemplateColumn(template_name = 'software/softwareLogo.html')
    edit = tables.TemplateColumn(template_name = 'software/softwareButtons.html')

    class Meta:
        model = Software
        template_name = 'django_tables2/bootstrap.html'
        fields = ('name', 'image')
        # 'sequence' is used to define the order in which columns appear
        sequence = ('logo', 'name', 'image', 'edit')

class CustomerSoftwareTable(tables.Table):
    # A regular column with an accessor allows for displaying properties of objects
    # In this case, we are displaying ForiegnKey variables
    customer_ID = tables.Column(accessor='cid.id', verbose_name='Customer ID')
    customer_Name = tables.Column(accessor='cid.name', verbose_name='Customer Name')
    software_ID= tables.Column(accessor='sid.id', verbose_name='Software ID')
    logo = tables.TemplateColumn(template_name = 'customersoftware/softwareLogo.html')
    software_Name = tables.Column(accessor='sid.name', verbose_name='Software Name')
    edit = tables.TemplateColumn(template_name = 'customersoftware/customersoftwareButtons.html')

    class Meta:
        model = CustomerSoftware
        template_name = 'django_tables2/bootstrap.html'
        fields = ('customer_ID', 'customer_Name', 'software_ID', 'logo', 'software_Name', 'edit')
        sequence = ('customer_ID', 'customer_Name', 'software_ID', 'logo', 'software_Name', 'edit')