from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.db.models import Q, Count
from django.http import HttpResponseRedirect

import requests
import json
from tester.serializers import UserSerializer, ManagerSerializer, ReviewSerializer, RoomSerializer, IconSerializer, OptionSerializer
from tester.models import User, Manager, Review, Room, Icon, Option

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


def main(request):
    # 쿠키에 토큰이 있다면 해당 토큰으로 로그인을 시도한다. == 토큰으로 값을 받아올 수 있는지 확인한다.
    # 이미 로그인 한 사이트에 대해, 창을 닫지 않는 한(탭만 닫았던 경우) 자동으로 로그인 되도록 하는 기능이다.
    if request.COOKIES.get('token'):
        token = request.COOKIES['token']
        # 토큰의 정보를 받는다.
        a = requests.get('https://kapi.kakao.com/v1/user/access_token_info', headers={'Authorization': 'Bearer '+token}).json()
        # 경고 메시지를 받은 경우 == 토큰이 유효하지 않은 경우이다.
        if a.get('msg'):
            return render(request, 'base.html', {'alive': 'false'})
        # 토큰이 유효하다면 해당 토큰의 회원번호를 사용해, 회원의 retrieve 뷰를 이용하여 회원 정보를 구한다.
        else:
            user = requests.get('http://127.0.0.1:8000/test/user/'+str(a.get('id'))+'/').json()
            # 로그인 상태임을 나타내는 변수와 함께, 접속한 회원의 닉네임을 context로 함께 전달한다.
            return render(request, 'base.html', {'alive': 'true', 'user': 'hi'})
    # 토큰이 쿠키에 없는 경우 == 로그인이 안 되는 경우
    else:
        # 그냥 메인 페이지로 이동한다.
        return render(request, 'base.html', {'alive': 'false'})


# 로그인 시도 시에 처리되는 메소드
def login(request):
    # 쿠키의 토큰이 암호화되어 있지 않다고 가정
    token = request.COOKIES.get('token')
    code = dict(request.GET).get('code')

    # 토큰이 쿠키에 있지만 만료되었다면 토큰을 None으로 바꾼다.
    # 페이지마다 별도로 쿠키를 관리하기 때문에 우연히 토큰이 만료되었음에도 쿠키가 남는 경우가 생길 수 있다.
    if token != None:
        if requests.get('https://kapi.kakao.com/v1/user/access_token_info', headers={'Authorization': 'Bearer ' + token}).json().get('msg'):
            token = None
    # 쿠키에 토큰이 없다면 새로 만들도록 한다.
    if token is None:
        # 로그인 창을 거치지 않았다면 로그인 창으로 이동시킨다. 만약 카카오 로그인이 되어있다면 바로 이 메소드로 돌아온다.
        if code == None:
            return HttpResponseRedirect('https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=dc1611725046556aa00ee3cd0fcc253f&redirect_uri=http://127.0.0.1:8000/test/login&response_type=code')
        # 로그인 창을 거쳤다면 인가코드를 갖고 있다.
        else:
            # 인가코드로 토큰을 받기 위해 변수들을 설정한다.
            # 권한 타입은 코드를 이용하는 방식으로 지정한다.
            grant_type = 'authorization_code'
            # 클라이언트 아이디는 REST api 키를 이용한다.
            client_id = 'dc1611725046556aa00ee3cd0fcc253f'
            # 이 메소드를 실행시키기 위한 URI를 준다.
            redirect_uri = 'http://127.0.0.1:8000/test/login'
            # 변수들을 합쳐서 하나의 데이터로 만든다.
            param = {
                'grant_type': grant_type,
                'client_id': client_id,
                'redirect_uri': redirect_uri,
                'code': code,
            }
            # 토큰을 받기 위한 URL이다.
            url = 'https://kauth.kakao.com/oauth/token'
            # 변수들을 주고 반환값을 얻는다.
            r = requests.post(url, data=param)
            json_result = r.json()
            # 반환값 중에서 액세스 토큰을 얻는다.
            token = json_result['access_token']

    # 쿠키에 토큰이 있었거나, 새로 발급 받은 경우 여기로 와서 토큰으로 정보를 받는다.
    a = requests.get('https://kapi.kakao.com/v1/user/access_token_info', headers={'Authorization': 'Bearer ' + token}).json()
    # 토큰 정보 중 회원 정보를 이용하여 해당 회원이 가입되어 있는지 확인한다.
    user = requests.get('http://127.0.0.1:8000/test/user/' + str(a.get('id')) + '/').json()
    # 토큰에 해당하는 회원이 DB에 없다면 회원 가입 페이지로 이동한다.
    if user.get('detail') == 'Not found.':
        res = render(request, 'sign_up.html')
        res.set_cookie('token', token, max_age=18000)
        return res
    # 메인 페이지로 이동하는 render를 생성한다.
    res = render(request, 'base.html', {'alive': 'true'})
    # 토큰을 쿠키로 추가한다. 쿠키는 5시간만 지속되도록 한다.
    res.set_cookie('token', token, max_age=18000)
    return res


def logout(request):
    # 현재 토큰을 쿠키에서 구한다.
    token = request.COOKIES.get('token')
    # 토큰의 상태를 확인한다.
    a = requests.get('https://kapi.kakao.com/v1/user/access_token_info', headers={'Authorization': 'Bearer ' + token}).json()
    # 오류 메시지를 받지 않는다면 로그아웃(토큰에 해당하는 아이디 만료시키기)을 한다.
    if not a.get('msg'):
        requests.post('https://kapi.kakao.com/v1/user/logout', headers={"Authorization": 'Bearer '+token})
    # 토큰의 생존 여부를 false로 넣는다.
    res = render(request, 'base.html', {'alive': 'false'})
    # 쿠키에서 토큰을 제거한다.
    res.delete_cookie('token')
    return res


def signup(request):
    token = request.COOKIES.get('token')
    # 토큰으로 사용자 정보를 얻는다.
    a = requests.get('https://kapi.kakao.com/v2/user/me', headers={'Authorization': 'Bearer ' + token}).json()
    # 획득한 사용자 정보를 바탕으로 DB에 넣을 값들을 정한다.
    body = {
        'u_id': a.get('id'),
        'u_nickname': a.get('properties').get('nickname'),
        'u_email': a.get('kakao_account').get('email'),
        'u_access_token': token
    }
    # 새로운 회원을 DB에 추가하는 뷰를 수행한다.
    requests.post('http://127.0.0.1:8000/test/user/', data=body)
    # 메인 페이지에 기본 상태로 이동하는 render를 작성한다.
    res = render(request, 'base.html', {'alive': 'false'})
    # 만약 토큰이 쿠키에 존재한다면 쿠키에서 제거한다.
    res.delete_cookie('token')
    return res


def ajaxTest(request):
    manager = json.loads(requests.get('http://127.0.0.1:8000/test/manager/').text)
    print(manager)
    return render(request, 'test.html', {"manager": manager})
