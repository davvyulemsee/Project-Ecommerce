from . import views
from django.urls import include, path

app_name = 'catalog'

urlpatterns = [
    path('', views.all_products, name="all_products"),
    path('create_product/', views.create_product, name="create_product"),
    path('<slug:slug>', views.product_page, name="product_page"),
    path('products/', views.product_list_api, name='product_list'),
    path('api/search/', views.search_product, name="search_product"),

]