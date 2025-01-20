from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from discount_info.models import Discount
from product_info.models  import Product

class Order(models.Model):
    """Order model to manage purchases"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ]

    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discounted_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    applied_discount = models.ForeignKey(
        Discount,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def calculate_totals(self):
        """Calculate order totals including all discounts"""
        self.total_amount = sum(item.get_subtotal() for item in self.items.all())
        
        if self.applied_discount and self.applied_discount.is_active:
            self.discounted_total = self.applied_discount.apply_discount(float(self.total_amount))
        else:
            self.discounted_total = self.total_amount
        
        self.save()

    def __str__(self):
        return f"Order {self.order_number}"

class OrderItem(models.Model):
    """Individual items within an order"""
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_subtotal(self):
        """Calculate subtotal for the item"""
        return float(self.final_price) * self.quantity

    def calculate_final_price(self):
        """Calculate final price based on product type and quantity"""
        base_price = float(self.product.base_price)
        
        if self.product.product_type == 'seasonal' and hasattr(self.product, 'seasonal_details'):
            discount = self.product.seasonal_details.get_current_discount()
            self.final_price = base_price * (1 - discount)
            
        elif self.product.product_type == 'bulk' and hasattr(self.product, 'bulk_details'):
            bulk_details = self.product.bulk_details
            if self.quantity >= bulk_details.min_quantity:
                self.final_price = base_price * (1 - float(bulk_details.bulk_discount))
            else:
                self.final_price = base_price
        else:
            self.final_price = base_price
            
        self.unit_price = base_price
        self.save()

    def save(self, *args, **kwargs):
        if not self.final_price:
            self.calculate_final_price()
        super().save(*args, **kwargs)
        self.order.calculate_totals()