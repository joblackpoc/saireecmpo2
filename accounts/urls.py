from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),

    # User Profile
    path('profile/', views.user_profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),

    # Session Management
    path('terminate-session/<int:session_id>/', views.terminate_session, name='terminate_session'),
]
