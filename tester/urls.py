from rest_framework import routers
from django.urls import path
from tester import views

router = routers.SimpleRouter()
router.register('user', views.UserViewSets)
router.register('manager', views.ManagerViewSets)
router.register('review', views.ReviewViewSets)
router.register('room', views.RoomViewSets)

# 커스텀 뷰셋의 경우는 아래처럼 [HTTP 메소드 명 : 수행할 함수 명] 형태로 필요한 함수들을 매핑한 형태작성할 수 있습니다.
"""
UserRetrieve = views.UserRetrieveViewSets.as_view({
    'post': 'retrieve'
})
"""


class UserRetrieveRouter(routers.SimpleRouter):
    routes = [
        routers.Route(
            url=r'^{prefix}/$',
            mapping={'post': 'retrieve'},
            name='{basename}',
            detail=False,
            initkwargs={'suffix': 'Detail'}
        )
    ]

router2 = UserRetrieveRouter()
router2.register('user_ret', views.UserRetrieveViewSets)

"""
urlpatterns = [
    path('user_ret/', UserRetrieve, name='user-retrieve'),
]
"""

urlpatterns = []

urlpatterns += router.urls
urlpatterns += router2.urls
