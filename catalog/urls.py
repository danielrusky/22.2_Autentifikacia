from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import product, create_category, create_product, ProductListView, ContactsView, ProductDetailView, \
    CategoryCreateView, ProductCreateView, CategoryListView, CategoryView, CategoryUpdateView, CategoryDeleteView, \
    ProductUpdateView, ProductDeleteView, CategoryDetailView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('product_create/', ProductCreateView.as_view(), name='create_product'),
    path('view_product/<int:pk>', ProductDetailView.as_view(), name='view_product'),
    path('edit_product/<int:pk>', ProductUpdateView.as_view(), name='edit_product'),
    path('delete_product/<int:pk>', ProductDeleteView.as_view(), name='delete_product'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('create_category/', CategoryCreateView.as_view(), name='create_category'),
    path('category_products/<int:pk>/', CategoryView.as_view(), name='category_products'),
    path('view_category/<int:pk>', CategoryDetailView.as_view(), name='view_category'),
    path('edit_category/<int:pk>/', CategoryUpdateView.as_view(), name='edit_category'),
    path('delete_category/<int:pk>/', CategoryDeleteView.as_view(), name='delete_category'),
]
