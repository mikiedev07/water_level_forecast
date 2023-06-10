from django.urls import path

from .views import graph_view

urlpatterns = [
    path('graph/', graph_view, name='graph'),
]
