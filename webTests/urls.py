"""webPages URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from webTests import views

urlpatterns = [
    path('base/', views.base),
    path('normal_user_base/', views.normal_user_base),
    path('normal_user_review_search/', views.normal_user_review_search),
    path('normal_user_review_write/', views.normal_user_review_write),
    path('normal_user_review_write_page/', views.normal_user_review_write_page),
    path('normal_user_review_read/', views.normal_user_review_read),
    path('image_test/', views.image),
    path('normal_user_review_search_test/', views.review_search_page),
    path('normal_user_review_search_testing/', views.review_search_test, name='searchTest'),
]