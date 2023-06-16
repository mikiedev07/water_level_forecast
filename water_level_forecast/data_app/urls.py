from django.urls import path

from .views import graph_view

urlpatterns = [
    path('chart/', graph_view, name='chart'),
]
