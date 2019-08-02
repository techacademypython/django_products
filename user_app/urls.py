from django.urls import path
from .views import register_view, login_view, logout_view

urlpatterns = [
    path('', login_view, name="login_view"),
    path('register/', register_view, name="register"),
    path('logout/', logout_view, name="logout_view"),
]
