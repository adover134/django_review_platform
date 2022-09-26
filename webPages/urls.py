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
from django.urls import path, include, re_path
from webPages import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    re_path(r'^$', views.main, name='main'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('loginPage/', views.loginPage, name='loginPage'),
    path('signup/', views.signup, name='signup'),
    path('infoCheck/', views.infoCheck, name='infoCheck'),
    path('normalUserReviewSearch/', views.normal_user_review_search, name='normalUserReviewSearch'),
    path('normal_user_review_write_page/', views.normal_user_review_write_page),
    path('normal_user_review_read/', views.normal_user_review_read, name='normalUserReviewRead'),
    path('toggleRecommmend/', views.normal_user_review_recommend, name='normalUserReviewRecommend'),
    path('toggleReport/', views.normal_user_review_report, name='normalUserReviewReport'),
    path('room_with_reviews_display/', views.room_with_reviews_display),
    path('change_user_info/', views.change_user_info),
    path('normal_user_review_list/', views.check_user_reviews, name='wroteReviews'),
    path('normal_user_room_test/', views.room_test, name='roomTest'),
    path('normal_user_room_search/', views.room_search, name='roomSearch'),
    path('db/', include('DBs.urls')),
    path('test/', include('webTests.urls')),
    path('review_search/', views.review_search, name='reviewTest')
]
