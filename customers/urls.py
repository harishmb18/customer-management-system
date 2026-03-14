from django.urls import path
from . import views

urlpatterns = [

    path('', views.customer_list, name='customer_list'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('add/', views.add_customer, name='add_customer'),

    path('<int:id>/edit/', views.edit_customer, name='edit_customer'),

    path('<int:id>/delete/', views.delete_customer, name='delete_customer'),

    path('export/', views.export_customers, name='export_customers'),

]