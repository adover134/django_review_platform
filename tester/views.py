from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from tester.serializers import UserSerializer, ManagerSerializer, ReviewSerializer, RoomSerializer
from tester.models import User, Manager, Review, Room

class UserViewSets(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, args, kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        # url의 lookup 필드를 통해 모델에서 가져온 인스턴습입니다.
        instance = self.get_object()

        #인스턴스의 데이터를 dictionary 자료형으로 직렬화하였습니다.
        data = self.get_serializer(instance).data

        #request.data의 자료형이 QueryDict이라 dict로 바꿔줍니다.
        data1 = dict(request.data)

        #입력 받은 값들에 대해서만 수정을 진행합니다.
        #form을 통해 입력받으면 각 필드가 배열 형태로 들어옵니다.
        for key in data1:
            #확인용 출력 라인입니다.
            print(data1[key])
            if data1[key][0] != '':
                data[key] = data1[key][0]

        """
        이 아래는 request.data가 QueryDict라는 자료형이라 바꿀 수 없어서
        여기서 update를 처리하려고 상위 함수의 코드를 가져왔습니다.
        """
        partial = kwargs.pop('partial', False)

        # 조작을 통해 생성한 값을 data로 넣어줍니다.
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, args, kwargs)


class ManagerViewSets(ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

    def retrieve(self, request, *args, **kwargs):
        data = request.GET['m_tel']
        print(data)
        instance = Manager.objects.get(m_tel=data)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, args, kwargs)

    def tere(self, request, *args, **kwargs):
        return super().destroy(self, request, args, kwargs)


class UserRetrieveViewSets(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def search(self, request, *args, **kwargs):
        data = User.objects.get(u_nickname=request.data['u_nickname'])
        serializer = self.get_serializer(data)
        return Response(serializer.data)


class ReviewViewSets(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, args, kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, args, kwargs)


class RoomViewSets(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, args, kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, args, kwargs)
