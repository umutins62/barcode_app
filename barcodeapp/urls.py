from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_barcode, name='create_barcode'),
    path('sil/<int:pk>/', views.delete_barcode, name='sil'),
    path('kaydet/<int:pk>/', views.save_barcode, name='kaydet'),
]
