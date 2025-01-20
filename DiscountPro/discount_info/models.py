from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Discount(models.Model):
    """Base discount model"""
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage Discount'),
        ('fixed', 'Fixed Amount Discount'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def apply_discount(self, price):
        """
        Apply discount to the given price. To be implemented by child classes.
        """
        if hasattr(self, 'percentage_discount'):
            return self.percentage_discount.apply_discount(price)
        elif hasattr(self, 'fixed_discount'):
            return self.fixed_discount.apply_discount(price)
        return price

class PercentageDiscount(models.Model):
    """Percentage-based discount implementation"""
    discount = models.OneToOneField(
        Discount,
        on_delete=models.CASCADE,
        related_name='percentage_discount'
    )
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        help_text="Discount percentage (0-100)"
    )
    min_purchase_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )

    def apply_discount(self, price):
        """Apply percentage discount to price"""
        if price < self.min_purchase_amount:
            return price
        
        discount_amount = (Decimal(str(price)) * self.percentage) / Decimal('100')
        return float(Decimal(str(price)) - discount_amount)

class FixedDiscount(models.Model):
    """Fixed amount discount implementation"""
    discount = models.OneToOneField(
        Discount,
        on_delete=models.CASCADE,
        related_name='fixed_discount'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    min_purchase_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )

    def apply_discount(self, price):
        """Apply fixed amount discount to price"""
        if price < self.min_purchase_amount:
            return price
            
        return float(max(Decimal(str(price)) - self.amount, Decimal('0')))