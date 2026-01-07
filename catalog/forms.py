from django import forms
from .models import Category, Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows':7}),
            'category': forms.Select(),

        }

