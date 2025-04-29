from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)                      # Item Name
    item_code = models.CharField(max_length=50, unique=True)     # Unique code like ITM00123
    category = models.CharField(max_length=50)                   # e.g., Bearings, Actuators
    part_number = models.CharField(max_length=100, blank=True)   # Manufacturer part number
    description = models.TextField(blank=True)                   # Optional long description

    quantity_in_stock = models.PositiveIntegerField(default=0)   # Current qty in warehouse
    reorder_level = models.PositiveIntegerField(default=10)      # Alert if below this level
    unit = models.CharField(max_length=20, default='pcs')        # pcs, kg, meter, etc.

    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)  # Cost to buy
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)   # Optional

    location = models.CharField(max_length=100, blank=True)      # e.g., Rack A2, Bin 5
    supplier_name = models.CharField(max_length=100, blank=True) # Supplier/brand
    last_updated = models.DateTimeField(auto_now=True)           # Auto timestamp

    is_active = models.BooleanField(default=True)                # Soft delete toggle

    def __str__(self):
        return f"{self.name} ({self.item_code})"
