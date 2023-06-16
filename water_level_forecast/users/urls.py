from django.urls import path
from .views import register, activate, user_login, logout_view

urlpatterns = [
    path('register/', register, name="signup"),
    path('login/', user_login, name="signin"),
    path('logout/', logout_view, name="signout"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]
