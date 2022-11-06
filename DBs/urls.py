from rest_framework import routers
from django.urls import path
from DBs import views

router = routers.SimpleRouter()
router.register('user', views.UserViewSets)
router.register('review', views.ReviewViewSets)
router.register('room', views.RoomViewSets)
router.register('icon', views.IconViewSets)
router.register('recommend', views.RecommendViewSets)
router.register('report', views.ReportViewSets)
router.register('reviewImage', views.ReviewImageViewSets)
router.register('roomImage', views.RoomImageViewSets)
urlpatterns = [
    # path('manager/', manager_list, name='manager-list'),
    # path('manager/<str:pk>/', manager_detail, name='manager-detail'),
    path('mainPageReviews/', views.getMainPageReview),
]

urlpatterns += router.urls
# urlpatterns += router2.urls
