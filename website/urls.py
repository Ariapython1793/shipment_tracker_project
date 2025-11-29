# tracking/urls.py
from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('containers/', views.container_list, name='container_list'),
    path('containers/new/', views.container_create, name='container_create'),
    path('containers/<int:pk>/edit/', views.container_update, name='container_update'),
    path('containers/<int:pk>/delete/', views.container_delete, name='container_delete'),
    path('export/csv/', views.export_csv, name='export_csv'),
]
