from . import views
from django.urls import include, path

app_name = "storefront"

urlpatterns = [
    path("", views.index, name="index")
]