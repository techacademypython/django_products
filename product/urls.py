from django.urls import path
from .views import dasboard, add_data, update_view, delete_view, sales_view, \
    sales_update_view

urlpatterns = [
    path('', dasboard, name="dashboard"),
    path('product/<int:id>/update', update_view, name="update_view"),
    path('product/<int:id>/delete', delete_view, name="delete_view"),
    path('sales/', sales_view, name="sales_view"),
    path('sales/<int:id>/update', sales_update_view, name="sales_update"),
    path('test/', add_data, name="add_data"),
]
