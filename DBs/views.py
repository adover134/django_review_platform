from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.shortcuts import render
from django.db.models import Q, Count

import requests
import json
from DBs.serializers import UserSerializer, ManagerSerializer, ReviewSerializer, RoomSerializer, IconSerializer, OptionSerializer
from DBs.models import User, Manager, Review, Room, Icon, Option

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
        # url의 lookup 필드를 통해 모델에서 가져온 인스턴스입니다.
        instance = self.get_object()

        #인스턴스의 데이터를 dictionary 자료형으로 직렬화하였습니다.
        data = self.get_serializer(instance).data

        #request.data의 자료형이 QueryDict이라 dict로 바꿔줍니다.
        data1 = dict(request.data)

        #입력 받은 값들에 대해서만 수정을 진행합니다.
        #form을 통해 입력받으면 각 필드가 배열 형태로 들어옵니다.
        for key in data1:
            #확인용 출력 라인입니다.
            print(key, data1[key])
            print(type(data1[key]))
            if data1[key] is None:
                continue
            elif type(data1[key]) is int:
                data[key] = data1[key]
                continue
            elif type(data1[key]) is dict:
                print(data1[key])
                #icon에 대한 정보입니다. 해당 정보로 icon에 대한 create를 수행하는 POST 메소드를 실행 하면 됩니다.
                requests.post('http://127.0.0.1:8000/test/icon/', data=data1[key])
                break
            elif data1[key][0] != '':
                data[key] = data1[key]
        print(data)

        """
        이 아래는 request.data가 QueryDict라는 자료형이라 바꿀 수 없어서
        여기서 update를 처리하려고 상위 함수의 코드를 가져왔습니다.
        """
        partial = kwargs.pop('partial', False)

        # 조작을 통해 생성한 값을 data로 넣어줍니다.
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response("Update Success!")

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        data1 = dict(request.GET)
        if not data1:
            return super().list(self, request, args, kwargs)
        print(data1)
        if data1.get('icon'):
            print("icon")
        for i in data1:
            print(i, end=" : ")
            for j in data1[i]:
                print(j,end=" ")
        data2 = Room.objects.all()
        a = [1, 2]
        #for i in a:
        #    print(i)
        room_query = Q()
        room_query.add(Q(r_id=1), Q.OR)
        room_query.add(Q(r_id=2), Q.OR)
        data3 = Review.objects.filter(room_query)
        print()
        print(data3)
        #for r in data3:
        #    print(r.r_id.r_name)
        print(Icon.objects.all().values('rev_id').annotate(total=Count('rev_id')))
        return super().list(self, request, args, kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        icons = serializer.data
        for i in icons['icons']:
            requests.delete(i)
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
        instance = self.get_object()
        for r in instance.room.all():
            icons = r.origin_review.all()
            for i in icons:
                print(r.rev_id, i.icon_x)
        return super().retrieve(self, request, args, kwargs)

    def list(self, request, *args, **kwargs):
        # URL의 파라미터들을 사전형 배열로 받는다.
        data1 = dict(request.GET)
        # 별도의 검색조건이 없다면 모델의 모든 값을 반환한다.
        if not data1:
            return super().list(self, request, args, kwargs)
        # 검색 조건으로 쿼리를 만든다.
        query = Q()  # 메인 쿼리로, 최종 결과를 낼 때 사용한다.
        query_address = Q()  # 주소에 대한 쿼리이다.
        if data1.get('address'):
            for ad in data1['address']:
                query_address.add(Q(address__contains=ad), Q.OR)
        query_rea = Q()  # 공인중개사에 대한 쿼리이다.
        if data1.get('real_estate_agency'):
            for rea in data1['real_estate_agency']:
                query_rea.add(Q(real_estate_agency__contains=rea), Q.OR)
        # 만약 옵션에 대한 검색 조건이 있다면, 해당하는 옵션들에 대해 참조한 원룸 데이터를 검색한다.
        # 옵션 모델에 대한 기본 URL을 먼저 적는다.
        optionURL = 'http://127.0.0.1:8000/test/option/' + '?'
        # 옵션에 대한 검색 조건이 존재한다면 각 옵션에 대해 원룸 번호만을 가져다 쿼리를 만든다.
        query_option = Q()
            # 원룸 번호를 저장할 리스트이다.
        data2 = list()
        if data1.get('option_num'):
            print(data1['option_num'])
        if data1.get('option'):
            print(data1['option'])
            for o in data1['option']:
                optionData = json.loads(requests.get(optionURL+'option='+o).text)
                option_to_room = list()
                for d in optionData:
                    option_to_room.append(d['room_id'])
                if not data2 :
                    data2=option_to_room
                else :
                    data2=list(set(data2).intersection(set(option_to_room)))
        for i in data2:
            query_option.add(Q(room_id=i), Q.OR)
        query.add(query_address, Q.AND)
        query.add(query_rea, Q.AND)
        query.add(query_option, Q.AND)
        searched = Room.objects.filter(query)
        return Response(self.get_serializer(searched, many=True).data)


    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, args, kwargs)


class IconViewSets(ModelViewSet):
    queryset = Icon.objects.all()
    serializer_class = IconSerializer


class OptionViewSets(ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer

    def list(self, request, *args, **kwargs):
        # URL의 파라미터들을 사전형 배열로 받는다.
        data1 = dict(request.GET)
        # 별도의 검색조건이 없다면 모델의 모든 값을 반환한다.
        if not data1:
            return super().list(self, request, args, kwargs)
        # 검색 조건으로 쿼리를 만든다. 옵션은 옵션 이름만 조건으로 받으며, 받은 옵션 이름들 중 하나에 해당하는 옵션들을 검색한다.
        query = Q()
        for o in data1['option']:
            query.add(Q(option_name=o), Q.OR)
        # 완성된 쿼리로 검색을 수행한다.
        searched = Option.objects.filter(query)
        # 검색 결과를 반환한다.
        return Response(self.get_serializer(searched, many=True).data)


def ajaxTest(request):
    manager = json.loads(requests.get('http://127.0.0.1:8000/test/manager/').text)
    print(manager)
    return render(request, 'test.html', {"manager": manager})
