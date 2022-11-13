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
    path('normal_user_review_search/', views.normal_user_review_search, name='normalUserReviewSearch'),
    path('normal_user_review_write_page/', views.normal_user_review_write_page, name='normalUserReviewWrite'),
    path('normal_user_review_read/', views.normal_user_review_read, name='normalUserReviewRead'),
    path('toggleRecommmend/', views.normal_user_review_recommend, name='normalUserReviewRecommend'),
    path('toggleReport/', views.normal_user_review_report, name='normalUserReviewReport'),
    path('normal_user_review_list/', views.check_user_reviews, name='wroteReviews'),
    path('normal_user_room_write_page/', views.normal_user_room_write_page, name='normalUserRoomWritePage'),
    path('normal_user_room_write/', views.normal_user_room_write, name='normalUserRoomWrite'),
    path('normal_user_room_change/', views.normal_user_room_change, name='normalUserRoomChange'),
    path('normal_user_room_update/', views.normal_user_room_update, name='normalUserRRoomUpdate'),
    path('normal_user_room_read/', views.normal_user_room_read, name='roomRead'),
    path('normal_user_room_search/', views.room_search, name='normalUserRoomSearch'),
    path('db/', include('DBs.urls')),
    path('normal_user_review_write/', views.review_write, name='review_write'),
    path('normal_user_review_change/', views.normal_user_review_change, name='normalUserReviewChange'),
    path('normal_user_review_update/', views.normal_user_review_update, name='normalUserReviewUpdate'),
    path('normal_user_review_delete/', views.normal_user_review_delete, name='normalUserReviewDelete'),
    path('introduction/', views.introduction, name='introduction'),
    path('user_inactivated/', views.user_inactivated),
]
