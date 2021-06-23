from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('signup/',views.signup,name="sign_up"),
    path('signin/',auth_views.LoginView.as_view(template_name='signin.html'),name="sign_in"),
    path('signout/',auth_views.LogoutView.as_view(template_name='signout.html'),name="sign_out"),

]