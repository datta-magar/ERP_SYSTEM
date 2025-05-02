'''Datta outliar enhnaced code'''
# sales/models.py
from django.db import models
from django.utils import timezone
from inventory.models import BuildingMaterial

class Customer(models.Model):
    """Customer information"""
    name = models.CharField(max_length=100)
    address = models.TextField()
    gstin = models.CharField(max_length=15, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.name

class Bill(models.Model):
    """Main bill/invoice model"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bill_no = models.CharField(max_length=20, unique=True)
    date = models.DateField(default=timezone.now)
    
    # Site information
    site_address = models.TextField(blank=True, null=True)
    gstin_no = models.CharField(max_length=15, blank=True, null=True)
    
    # Totals (will be calculated from items)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    add_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # 2.5%
    sgst = models.DecimalField(max_digits=12, decimal_places=2, default=0)      # 2.5%
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Bill #{self.bill_no} - {self.customer.name}"
    
    def calculate_totals(self):
        """Calculate bill totals based on items"""
        # Calculate subtotal from all items
        items_total = sum(item.amount for item in self.items.all())
        self.total_amount = items_total
        
        # Calculate additional costs and taxes
        self.add_cost = round(self.total_amount * 0.025, 2)  # 2.5% additional cost
        self.sgst = round(self.total_amount * 0.025, 2)      # 2.5% SGST
        
        # Calculate grand total
        self.grand_total = self.total_amount + self.add_cost + self.sgst
        self.save()

class BillItem(models.Model):
    """Individual line items in a bill"""
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='items')
    date = models.DateField(default=timezone.now)
    challan_no = models.CharField(max_length=30, blank=True, null=True)
    material = models.CharField(max_length=100)  # Material name as text
    qty = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return f"{self.material} ({self.qty} @ {self.rate})"
    
    def save(self, *args, **kwargs):
        # Calculate amount
        self.amount = self.qty * self.rate
        super().save(*args, **kwargs)
        
        # Update bill totals
        self.bill.calculate_totals()
        