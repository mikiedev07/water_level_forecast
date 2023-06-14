from django.urls import path
from .views import register, activate, user_login

urlpatterns = [
    path('register/', register, name="signup"),
    path('login/', user_login, name="signin"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]
