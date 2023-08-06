from django.urls import path

app_name = 'django_hub_sdk'

from .views import LoginView, CallbackView, UserMeView, LogoutView

urlpatterns = [
    path("auth/login", LoginView.as_view(), name="login"),
    path("auth/logout", LogoutView.as_view(), name="logout"),
    path("auth/callback", CallbackView.as_view(), name="callback"),
    path("users/me", UserMeView.as_view(), name="me")
]
