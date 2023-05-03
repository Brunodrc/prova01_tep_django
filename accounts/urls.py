from django.urls import path
from . import views
urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path("user/signup/", views.user_signup, name='user_signup'),
    path("user/register/", views.user_register, name='user_register'),
    path("user/signin/", views.user_signin, name='user_signin'),
    path("user/login/", views.user_login, name='user_login'),
    path("user/logout/", views.user_logout, name='user_logout'),
]
