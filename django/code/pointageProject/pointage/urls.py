from django.urls import path
from . import views

urlpatterns = [
    path('pointage/', views.pointage_list, name='pointage-list'),
]