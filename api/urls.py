from django.contrib import admin
from django.urls import path, include
from api.views import SendPasswordResetEmailView, UserChangePasswordView, UserPasswordResetView, UserProfileView, UserRegistrationView, UserLoginView

app_name = 'api'

urlpatterns = [
    # Auth Urls
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('sendpasswordresetemail/', SendPasswordResetEmailView.as_view(), name='sendpasswordresetemail'),
    path('resetpassword/<uid>/<token>/', UserPasswordResetView.as_view(), name='resetpassword'),
    
     # adminviews
    path('getusers/', UsersListView.as_view(), name='getusers'),
]
