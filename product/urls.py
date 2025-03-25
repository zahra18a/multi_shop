from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('all', views.ProductsListView.as_view(), name='products_list'),
    path('navbar', views.NavbarPartialView.as_view(), name='navbar'),
]
