from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import login_view, registration_view, profile_view

app_name = 'users'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', LogoutView.as_view(next_page='/users/login/'), name='logout'),
    path('profile/', profile_view, name='profile'),
]
