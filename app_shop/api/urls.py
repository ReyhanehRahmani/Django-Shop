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
from app_shop.api import views

urlpatterns = [
    path('special-offer-list', views.special_offer_list ),
    path('product-create', views.product_create ),
    path('product-delete/<int:product_id>', views.product_delete ),
    path('product-update/<int:product_id>', views.product_update ),
    path('product/<int:product_id>', views.product_detail ),
    path('products/', views.ProductListView.as_view()),
    path('product-comment-list/<int:product_id>', views.product_comment_list),
    path('product/<int:product_id>/comment-create', views.CommentCreateView.as_view()),
    path('comment/<int:comment_id>', views.CommentUpdateDeleteView.as_view()),

]
