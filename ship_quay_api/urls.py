from django.urls import path
from . import views

urlpatterns = [
    path('list_quays/', views.list_quays, name='list_quays'),
    path('find_suitable_quay/<int:ship_id>/', views.find_suitable_quay, name='find_suitable_quay'),
    path('get_ship_details/<int:ship_id>/', views.get_ship_details, name='get_ship_details'),
]
