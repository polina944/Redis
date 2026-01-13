from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from sign.views import BaseRegisterView, ConfirmLogout

from sign.views import set_authors

urlpatterns = [

    path('signup/', BaseRegisterView.as_view(template_name='sign/signup.html'), name='signup'),

    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),

    path('confirm/logout/', ConfirmLogout.as_view(), name='confirm_logout'),

    path('set_authors/', set_authors, name='set_authors'),
]
