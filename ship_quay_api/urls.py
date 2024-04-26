from django.urls import path
from . import views

urlpatterns = [
    path("list_quays/", views.list_quays, name="list_quays"),
]
