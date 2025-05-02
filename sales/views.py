'''Datta outliar enhnaced code'''
# sales/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from django.db import transaction
from num2words import num2words

from .models import Customer, Bill, BillItem
from .forms import CustomerForm, BillForm, BillItemFormSet
from inventory.models import BuildingMaterial, StockTransaction

# For PDF generation
from xhtml2pdf import pisa
from io import BytesIO

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'sales/customer_list.html', {'customers': customers})

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer added successfully")
            return redirect('customer_list')
    else:
        form = CustomerForm()
    
    return render(request, 'sales/customer_form.html', {'form': form})

def bill_list(request):
    bills = Bill.objects.all().order_by('-date')
    return render(request, 'sales/bill_list.html', {'bills': bills})

def bill_detail(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    return render(request, 'sales/bill_detail.html', {'bill': bill})

@transaction.atomic
def bill_create(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        
        if form.is_valid():
            bill = form.save()
            
            # Process the formset (bill items)
            formset = BillItemFormSet(request.POST, instance=bill)
            
            if formset.is_valid():
                formset.save()
                
                # Update inventory for each item
                for form in formset:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        material_name = form.cleaned_data.get('material')
                        qty = form.cleaned_data.get('qty')
                        
                        # Try to find matching material in inventory
                        try:
                            material = BuildingMaterial.objects.filter(name__icontains=material_name).first()
                            if material:
                                # Create stock transaction
                                StockTransaction.objects.create(
                                    material=material,
                                    transaction_type='OUT',
                                    quantity=qty,
                                    reference=f"Bill #{bill.bill_no}"
                                )
                        except Exception as e:
                            print(f"Error updating inventory: {e}")
                
                messages.success(request, f"Bill #{bill.bill_no} created successfully!")
                return redirect('bill_detail', pk=bill.pk)
    else:
        form = BillForm()
        formset = BillItemFormSet()
    
    return render(request, 'sales/bill_form.html', {
        'form': form,
        'formset': formset,
    })

def render_to_pdf(template_src, context_dict):
    """Generate PDF from HTML template"""
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def generate_bill_pdf(request, pk):
    """Generate a PDF of the bill"""
    bill = get_object_or_404(Bill, pk=pk)
    
    # Convert amount to words
    amount_in_words = num2words(int(bill.grand_total), lang='en_IN').title()
    amount_in_words += " Rupees Only"
    
    context = {
        'bill': bill,
        'amount_in_words': amount_in_words,
    }
    
    pdf = render_to_pdf('sales/bill_pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"Bill_{bill.bill_no}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    return HttpResponse("Error generating PDF", status=400)
