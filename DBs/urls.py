from rest_framework import routers
from django.urls import path
from DBs import views

router = routers.SimpleRouter()
router.register('user', views.UserViewSets)
# router.register('manager', views.ManagerViewSets)
router.register('review', views.ReviewViewSets)
router.register('room', views.RoomViewSets)
router.register('icon', views.IconViewSets)
router.register('option', views.OptionViewSets)

"""
뷰셋을 직접 URL path로 경우는 아래처럼
[HTTP 메소드 명 : 수행할 함수 명] 형태로
필요한 함수들을 매핑한 형태작성할 수 있습니다.
"""
manager_list = views.ManagerViewSets.as_view({
    'get': 'list',
    'post': 'create',
})

"""
ManagerViewSets의 경우는 detail이라 하여 세부 항목에 대한 url이 따로 있었으므로
2개의 항목으로 나눠서 url을 만들어줍니다.
"""
manager_detail = views.ManagerViewSets.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'tere'
})


class UserRetrieveRouter(routers.SimpleRouter):
    routes = [
        routers.Route(
            url=r'^{prefix}/$',
            mapping={'post': 'search'},
            name='{basename}',
            detail=False,
            initkwargs={'suffix': 'Detail'}
        )
    ]

router2 = UserRetrieveRouter()
router2.register('user_ret', views.UserRetrieveViewSets)

"""
manager 에는 기본 기능들을,
manager 뒤에 회원 번호를 넣는 경우는 세부 기능을 수행하도록 2개의 패턴을 넣습니다.
<str:pk>는 해당 위치의 값이 view에서 읽을 때
kwargs의 pk:~ 형태의 값으로 들어가며 string 타입임을 명시한 것입니다.
기본적으로는 <int:pk>가 들어가며, 이는 pk 값이 들어가고 integer 타입임을 명시하는 겁니다.
"""
urlpatterns = [
    path('manager/', manager_list, name='manager-list'),
    path('manager/<str:pk>/', manager_detail, name='manager-detail'),
    path('ajaxTest/', views.ajaxTest),
]

urlpatterns += router.urls
urlpatterns += router2.urls
