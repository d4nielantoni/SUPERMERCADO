from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lista/nova/', views.create_list, name='create_list'),
    path('lista/<int:pk>/', views.list_detail, name='list_detail'),
    path('lista/<int:pk>/deletar/', views.delete_list, name='delete_list'),
    path('item/<int:pk>/toggle/', views.toggle_item, name='toggle_item'),
    path('item/<int:pk>/deletar/', views.delete_item, name='delete_item'),
]
