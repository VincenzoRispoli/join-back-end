from django.urls import path
from user_auth_app.api.views import RegistrationView
from rest_framework.authtoken.views import obtain_auth_token
from .views import CustomLoginView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login')
]
