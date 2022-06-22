import django_tables2 as tables
import django_tables2.utils as A
from CRUD_example.models import(
    Customer,
    Software,
    CustomerSoftware,
)

class CustomerTable(tables.Table):
    edit = tables.TemplateColumn(
        template_name = "customers/customerButtons.html"
    )

    class Meta:
        model = Customer
        template_name = 'django_tables2/bootstrap.html'
        fields = ('name', )


class SoftwareTable(tables.Table):
    logo = tables.TemplateColumn(
        template_name = 'software/softwareLogo.html'
    )
    edit = tables.TemplateColumn(
        template_name = 'software/softwareButtons.html'
    )

    class Meta:
        model = Software
        template_name = 'django_tables2/bootstrap.html'
        fields = ('name', 'image')
        sequence = ('logo', 'name', 'image', 'edit')