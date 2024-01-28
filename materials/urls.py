from django.urls import path

from materials.apps import MaterialsConfig
from catalog.views import ProductListView, ProductDetailView
from materials.views import MaterialCreateView, MaterialListView, MaterialDetailView, MaterialUpdateView, \
    MaterialDeleteView, toggle_active

app_name = MaterialsConfig.name

urlpatterns = [
    path('', MaterialListView.as_view(), name='list_material'),
    path('create_material/', MaterialCreateView.as_view(), name='create_material'),
    path('view_material/<int:pk>/', MaterialDetailView.as_view(), name='view_material'),
    path('edit_material/<int:pk>/', MaterialUpdateView.as_view(), name='edit_material'),
    path('delete_material/<int:pk>/', MaterialDeleteView.as_view(), name='delete_material'),
    path('to_published/<slug>', toggle_active, name='toggle_active')
]