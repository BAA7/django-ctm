"""
URL configuration for ctm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from main_app import views

urlpatterns = [
    re_path(r'^create-user', views.create_user, name='create_user'),
    re_path(r'^edit-user/', views.edit_user, name='edit_user'),
    re_path(r'^delete-user', views.delete_user, name='delete_user'),
    re_path(r'^login', views.sign_in, name='sign_in'),
    re_path(r'^logout', views.log_out, name='logout'),
    re_path(r'^users', views.users, name='users'),
    re_path(r'^admin', views.admin, name='admin'),
    re_path(r'^profile/', views.profile, name='profile'),
    path('', views.index, name='homepage'),
]
