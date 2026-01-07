from django.db import models
from django.utils import timezone
import uuid

# Create your models here.

class GuestCart(models.Model):
    token = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Guest Number {self.token}"

class GuestCartItem(models.Model):
    cart = models.ForeignKey(GuestCart, related_name='items', on_delete=models.CASCADE)
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(default = timezone.now)

    class Meta:
        unique_together = ('cart', 'product_id')

        
