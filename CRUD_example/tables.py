import django_tables2 as tables
import django_tables2.utils as A
from CRUD_example.models import(
    Customer,
    Software,
    CustomerSoftware,
)

class CustomerTable(tables.Table):
    edit = tables.TemplateColumn(template_name = "customers/customerButtons.html")

    class Meta:
        model = Customer
        template_name = 'django_tables2/bootstrap.html'
        fields = ('name', 'edit')


class SoftwareTable(tables.Table):
    logo = tables.TemplateColumn(template_name = 'software/softwareLogo.html')
    edit = tables.TemplateColumn(template_name = 'software/softwareButtons.html')

    class Meta:
        model = Software
        template_name = 'django_tables2/bootstrap.html'
        fields = ('name', 'image')
        sequence = ('logo', 'name', 'image', 'edit')

class CustomerSoftwareTable(tables.Table):
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