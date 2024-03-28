"""
URL configuration for master_copy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from masterapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('Account Manager/', views.Account_Manager, name='Account Manager'),
    path('Trade Copier/', views.Trade_Copier, name='Trade Copier'),
    path('Blog/', views.Blog, name='Blog'),
    path('Contact/', views.Contact, name='Contact'),
    path('Pricing/', views.Pricing, name='Pricing'),
    path('forgot-password/', views.forgot_password, name='forget_password'),
    path('reset-password/<int:user_id>/<str:token>/', views.reset_password, name='reset_password'),

    # Add other URL patterns as needed
    # path('forget_password/', views.forget_password, name='forget_password'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.home, name='home'),
]

