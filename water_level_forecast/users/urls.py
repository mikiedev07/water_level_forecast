from django.urls import path
from .views import register, activate, user_login, logout_view, analyst_page_view

urlpatterns = [
    path('register/', register, name="signup"),
    path('login/', user_login, name="signin"),
    path('logout/', logout_view, name="signout"),
    path('analyst-panel/', analyst_page_view, name="analyst_panel"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]
