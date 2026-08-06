"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from app_account.api import views

urlpatterns = [
    path('favorite-list', views.favorite_list ),
    path('favorite', views.favorite ),
    path('profile/', views.UserProfileDetailView.as_view(), name='profile-detail'),
    path('profile/create/', views.UserProfileCreateView.as_view(), name='profile-create'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='profile-update'),
    path('profile/delete/', views.UserProfileDeleteView.as_view(), name='profile-delete'),
    path('addresses/', views.AddressListView.as_view(), name='address-list-create'),
    path('addresses/<int:pk>/', views.AddressDetailView.as_view(), name='address-detail'),]

