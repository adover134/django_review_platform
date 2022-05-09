from rest_framework import routers
from django.urls import path
from tester import views

router = routers.SimpleRouter()
router.register('user', views.UserViewSets)
router.register('manager', views.ManagerViewSets)
router.register('review', views.ReviewViewSets)
router.register('room', views.RoomViewSets)
urlpatterns = [
    # path('some_functional_view_url', views.functional_view)
]
urlpatterns += router.urls
