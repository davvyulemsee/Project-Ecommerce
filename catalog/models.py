from django.db import models
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 100, unique=True)
    slug = models.SlugField(max_length=120, unique = True, blank=True)
    description = models.TextField(blank = True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    CATEGORY_CHOICES = [
    ("luggage", "Luggage"),
    ("bags", "Bags"),
    ("accessories", "Accessories"),
    ]
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=120, blank=True, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField( max_length=20, choices=CATEGORY_CHOICES )
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    featured = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)





