# accounts/urls.py
from django.urls import path
from .views import SignUpView, signup
from .views import LoginView
from . import views
app_name = 'accounts'

urlpatterns = [
    path('api/accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/', signup, name='signup_page'),
    path('api/accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('register/', views.register, name ='register'),
]
