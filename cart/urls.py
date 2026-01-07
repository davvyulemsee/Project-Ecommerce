from . import views
from django.urls import include, path

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name="cart"),
    path('add/<int:product_pk>/', views.add_to_cart, name='add'),
    path('update/<int:product_pk>/', views.update_cart_item, name='update'),
    path('remove/<int:product_pk>/', views.remove_cart_item, name='remove'),
    path('checkout', views.checkout, name='checkout'),
    path('pay_mpesa', views.pay_mpesa, name='pay_mpesa')

]