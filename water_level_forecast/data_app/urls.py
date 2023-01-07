from django.urls import path

from .views import *

urlpatterns = [
    path('data/', admin.site.urls),
]