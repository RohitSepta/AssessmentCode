from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime

class Product(models.Model):
    """Base product model"""
    PRODUCT_TYPES = [
        ('seasonal', 'Seasonal Product'),
        ('bulk', 'Bulk Product'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPES
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ${self.base_price}"

class SeasonalProduct(models.Model):
    """Seasonal product specific attributes"""
    SEASONS = [
        ('SPRING', 'Spring'),
        ('SUMMER', 'Summer'),
        ('FALL', 'Fall'),
        ('WINTER', 'Winter'),
    ]

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='seasonal_details'
    )
    season = models.CharField(max_length=10, choices=SEASONS)
    season_discount = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    off_season_discount = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    def get_current_discount(self):
        current_month = datetime.now().month
        season_months = {
            'SPRING': [3, 4, 5],
            'SUMMER': [6, 7, 8],
            'FALL': [9, 10, 11],
            'WINTER': [12, 1, 2]
        }
        return float(self.season_discount if current_month in season_months[self.season] 
                    else self.off_season_discount)

class BulkProduct(models.Model):
    """Bulk product specific attributes"""
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='bulk_details'
    )
    min_quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    bulk_discount = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )