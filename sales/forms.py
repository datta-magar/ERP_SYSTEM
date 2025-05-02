'''Datta outliar enhnaced code'''
# sales/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Customer, Bill, BillItem

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'address', 'gstin', 'phone']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['customer', 'bill_no', 'date', 'site_address', 'gstin_no']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'site_address': forms.Textarea(attrs={'rows': 3}),
        }

class BillItemForm(forms.ModelForm):
    class Meta:
        model = BillItem
        fields = ['date', 'challan_no', 'material', 'qty', 'rate']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

# Create a formset for multiple bill items
BillItemFormSet = inlineformset_factory(
    Bill, 
    BillItem,
    form=BillItemForm,
    extra=5,  # Start with 5 empty forms
    can_delete=True
)
