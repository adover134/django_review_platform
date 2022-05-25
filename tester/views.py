from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.shortcuts import render
from django.db.models import Prefetch
import requests
import json
from tester.serializers import UserSerializer, ManagerSerializer, ReviewSerializer, RoomSerializer
from tester.models import User, Manager, Review, Room

class UserViewSets(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # 회원 별로, 작성한 리뷰들에 대해 역참조를 하여 리뷰 내용을 받아오도록 해봤습니다.
    def retrieve(self, request, *args, **kwargs):
        # 15~18번 줄은 조인을 하지 않은 코드입니다. 18번 줄에서, 각 writer에 대해 하위 값을 찾을 때마다 쿼리를 한 번씩
        instance = self.get_object()
        for r in instance.writer.all():
            print(r.review)
        print("=======")
        #20~23번 줄은 조인을 한 코드입니다. 22번 줄에서 미리 모든 writer 항목에 대해 review 값을 받아옵니다.
        instance2 = User.objects.filter(u_id=instance.u_id).prefetch_related('writer')[0]
        for r in instance2.writer.all():
            print(r.review)
        return super().retrieve(self, request, args, kwargs)

    def addWarnCount(u_id):
        """
        REST api니까 값을 request를 통해 받아야 한다고 생각하였습니다.
        retrieve 메소드를 이용하여 해당하는 User 정보를 얻습니다.
        값을 텍스트로 읽은 후 json으로 바꿔줬습니다.
        그 후, 필요한 값인 u_warn_count를 data로 지정하였습니다.
        마지막으로, update 메소드에 u_warn_count를 기존 값 + 1로 하여 보냅니다.
        """
        instance = json.loads(requests.get('http://127.0.0.1:8000/test/user/' + u_id + '/').text)
        print(instance)
        data = instance['u_warn_count']
        print(data)
        requests.put('http://127.0.0.1:8000/test/user/' + u_id + '/', data={'u_warn_count': data+1})

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
        u_id = serializer.data['u_id']
        """
        새로 추가한 메소드인 addWarnCount를 실행시킵니다.
        인자로 위에서 구한 u_id를 줍니다.
        """
        u_warn_count = json.loads(requests.get('http://127.0.0.1:8000/test/user/' + u_id + '/').text)['u_warn_count']
        print(type(u_warn_count))
        requests.put('http://127.0.0.1:8000/test/user/' + u_id + '/', data={'u_warn_count': u_warn_count + 1})
        # UserViewSets.addWarnCount(u_id)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, args, kwargs)

    def tere(self, request, *args, **kwargs):
        print("good-bye")
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

    def list(self, request, *args, **kwargs):
        return super().list(self, request, args, kwargs)

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


def main(request):
    return render(request, 'test.html', {'manager':json.loads(requests.get('http://127.0.0.1:8000/test/manager/').text)})