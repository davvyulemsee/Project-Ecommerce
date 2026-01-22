from django.shortcuts import render, redirect, get_object_or_404

from .forms import ProductForm
from .models import Product
from .models import Category
from django.http import JsonResponse
from .models import Product
from .serializers import ProductSerializer
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:all_products')
    else:
        form = ProductForm()
    return render(request, 'catalog/createproduct.html', {'form':form})

def all_products(request):
    category = request.GET.get('category')
    query = request.GET.get('q')

    products = Product.objects.all()
    if category:
        products = products.filter(category__iexact=category)
    if query:
        products = products.filter(name__icontains = query)

    return render(request, 'catalog/categorypage.html',
                  {
        'products': products,
        'category': category,
        "categories": dict(Product.CATEGORY_CHOICES),
                  })

def product_page(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'catalog/productpage.html', {
        'product':product,
    })

def product_list_api(request):
    products = Product.objects.all()
    data = []

    for p in products:
        data.append({
            'id':p.id,
            'name':p.name,
            'price':str(p.price),
            'category':p.category,
        })
    return JsonResponse({'products':data})

@api_view(['GET'])
# @permission_classes([AllowAny])
def search_product(request):
    queryset = Product.objects.all()
    query = request.GET.get('q', '').strip()

    if not query:
        return Response({"error": "Please provide search terms with q="}, status = 400)


    queryset = queryset.filter(
        Q(name__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query)
    )

    category = request.GET.get('category')
    if category:
        queryset = queryset.filter(category__icontains=category)

    limit = request.GET.get("limit", 5)
    products = queryset[:int(limit)]

    serializer = ProductSerializer(products, many=True)

    return Response({
        "length":len(serializer.data),
        "Content": serializer.data
    }, content_type='application/json')