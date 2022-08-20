from django.http import HttpResponse
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.shortcuts import render
from django.db.models import Q, Count

import datetime

import requests
import json
import copy
from DBs.serializers import UserSerializer, ManagerSerializer, ReviewSerializer, ReviewSerializer2, RoomSerializer, IconSerializer, RecommendSerializer, ReportSerializer, CommonInfoSerializer, ImageSerializer
from DBs.models import User, Manager, Review, Room, Icon, Recommend, Report, CommonInfo, Image
from DBs.services import sentence_spliter


class UserViewSets(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, args, kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        # URL의 lookup 필드에 해당하는 값으로 모델에서 인스턴스를 꺼낸다.
        instance = self.get_object()
        # 인스턴스의 값들을 해당하는 모델에 대한 시리얼라이저로 직렬화한다.
        data1 = self.get_serializer(instance).data
        # request로 받은 데이터를 dictionary 값으로 변수에 넣는다.
        data2 = dict(request.data)
        # data1에서 입력받은 값들만 변환한다.
        for key in data2:
            if data2[key] != '':
                data1[key] = data2[key][0] # (입력받은 값들은['']의 형태로 배열로 들어온다.)
        # 갱신된 인스턴스를 직렬화한다.
        serializer = self.get_serializer(instance, data=data1)
        # 시리얼라이저의 유효 여부를 검사한다.
        serializer.is_valid(raise_exception=True)
        # 모델에 갱신된 인스턴스 정보를 저장한다.
        self.perform_update(serializer)
        # 갱신이 성공했음을 반환한다.
        return Response("Update Success!")

    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, args, kwargs)


class ManagerViewSets(ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, args, kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, args, kwargs)

    def update(self, request, *ars, **kwargs):
        # URL의 lookup 필드에 해당하는 값으로 모델에서 인스턴스를 꺼낸다.
        instance = self.get_object()
        # 인스턴스의 값들을 해당하는 모델에 대한 시리얼라이저로 직렬화한다.
        data1 = self.get_serializer(instance).data
        # request로 받은 데이터를 dictionary 값으로 변수에 넣는다.
        data2 = dict(request.data)
        # data1에서 입력받은 값들만 변환한다.
        for key in data2:
            if data2[key] != '':
                data1[key] = data2[key][0] # (입력받은 값들은['']의 형태로 배열로 들어온다.)
        # 갱신된 인스턴스를 직렬화한다.
        serializer = self.get_serializer(instance, data=data1)
        # 시리얼라이저의 유효 여부를 검사한다.
        serializer.is_valid(raise_exception=True)
        # 모델에 갱신된 인스턴스 정보를 저장한다.
        self.perform_update(serializer)
        # 갱신이 성공했음을 반환한다.
        return Response("Update Success!")

    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, args, kwargs)


class ReviewViewSets(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        # 입력값을 data로 저장한다.
        data = copy.deepcopy(request.data)
        # 입력값에 리뷰 종류가 없다면 에러를 반환한다. 아니라면 리뷰 종류를 저장한다.
        reviewKind = None
        if not data.get('reviewKind'):
            return Response('create_failed')
        else:
            reviewKind = int(data.get('reviewKind'))
            if (reviewKind != 0) and (reviewKind != 1):
                return Response('create_failed')
        # 입력값 중 아이콘에 대한 것을 제외하고 data1으로 저장한다.
        data1 = {}
        data1['reviewKind'] = int(data.get('reviewKind'))
        data1['reviewTitle'] = data.get('reviewTitle')
        data1['roomId'] = int(data.get('roomId'))
        data1['uId'] = data.get('uId')
        # 입력값의 종류에 따라 아이콘에 대한 입력 방식이 달라진다.
        # 텍스트 리뷰인 경우
        if reviewKind == 0:
            data1['reviewSentence'] = sentence_spliter(data.get('reviewSentence'))
            # 시각화 모듈 이용해 리뷰 본문 텍스트로 아이콘 생성 및 저장한다.
            # 시각화모듈(data['reviewSentence'])
        # 이미지 리뷰인 경우
        else:
            # 리뷰 본문을 입력받을 변수를 선언한다.
            reviewSentence = ''
        # 입력 값 중, dictionary타입인 값은 전부 icon이다.
            for key in data:
                if type(data[key]) is dict:
                    icon = data[key]
                    # 아이콘의 주석들을 합쳐서 본문을 작성한다.
                    reviewSentence = reviewSentence +icon['iconInformation']
            # data1에 리뷰 본문을 추가한다.
            data1['review_sentence'] = reviewSentence
        # 완성된 리뷰 정보를 시리얼라이저로 직렬화한다.
        serializer = self.get_serializer(data=data1)
        # 시리얼라이저가 유효하면 저장한다.
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        headers = self.get_success_headers(serializer.data)
        review_id = review.id
        if reviewKind == 1:
            for key in data:
                if type(data[key]) is dict:
                    icon = data[key]
                    # 아이콘 정보에 리뷰 번호를 추가한다.
                    icon['revId'] = review_id
                    # 입력받은 데이터로 새 아이콘을 생성하는 POST 메소드를 수행한다.
                    # requests.post('http://127.0.0.1:8000/db/icon/', data=icon)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        # URL의 파라미터들을 사전형 배열로 받는다.
        data1 = dict(request.GET)
        # 별도의 검색조건이 없다면 모델의 모든 값을 반환한다.
        if not data1:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = ReviewSerializer2(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = ReviewSerializer2(queryset, many=True)
            return Response(serializer.data)
        # 검색 조건을 쿼리로 만들어 저장할 변수를 만든다.
        query = Q()

        # 회원 닉네임을 받았다면 해당하는 회원의 리뷰만 찾는 쿼리를 만들어 최종 쿼리에 더한다.
        if data1.get('uNickname'):
            query_user_nickname = Q(uNickname=data1['uNickname'])
            query.add(query_user_nickname, Q.AND)
        # 작성일의 시작점과 끝점을 받았다면 해당 기간 동안 작성된 리뷰만 찾는 쿼리를 만들어 최종 쿼리에 더한다.
        if data1.get('date'):
            query_date = Q(reviewDate__range=[int(data1['date'][0]), int(data1['date'][1])])
            query.add(query_date, Q.AND)
        # 리뷰 종류를 받았다면 해당하는 종류의 리뷰만 찾는 쿼리를 만든다.
        if data1.get('kind'):
            query_kind = Q(reviewKind=data1['kind'])
            query.add(query_kind, Q.AND)
        # 최소 추천 수를 받았다면 그 이상의 추천을 갖는 리뷰만 찾는 쿼리를 만든다.
        if data1.get('recommend'):
            query_recommend = Q()
            # 추천들을 리뷰 단위로 묶어서 리뷰 번호와 개수를 구한다.
            recommends = Recommend.objects.all().values('revId').annotate(total=Count('revId')).order_by('total')
            # 각 그룹에 대해서 추천 수가 일정 이상인 경우만 구하는 쿼리를 만든다.
            if recommends[0]['total'] >= data1['recommend']:
                for rec in recommends:
                    if rec['total'] >= data1['recommend']:
                        query_recommend.add(Q(revId=rec['revId']), Q.OR)
                    else:
                        break
                query.add(query_recommend, Q.AND)
        # 최소 신고 수를 받았다면 그 이상의 신고를 받은 리뷰만 찾는 쿼리를 만든다. 방법은 추천과 같다.
        if data1.get('report'):
            query_report = Q()
            reports = Report.objects.all().values('revId').annotate(total=Count('revId')).order_by('total')
            if reports[0]['total'] >= data1['report']:
                for rep in reports:
                    if rep['total'] >= data1['report']:
                        query_report.add(Q(revId=rep['revId']), Q.OR)
                    else:
                        break
                query.add(query_report, Q.AND)
        # 아이콘 정보로 조회하는 쿼리를 만들어 추가한다.
        if data1.get('icon'):
            query_icon = Q()
            query.add(query_icon, Q.AND)
        searched = None

        ###############################################################
        # 원룸 ID를 받았다면 해당 원룸 ID와 동일한 리뷰 쿼리(검색과 별개로 조회시)
        if data1.get('roomId'):
            rId = data1.get('roomId')[0]
            rId = rId[:-1]
            query_roomId = Q(roomId_id=rId)

            query.add(query_roomId, Q.AND)
            searched = Review.objects.filter(query)

            #Serializer 별도 설정
            serializer = ReviewSerializer(searched, context={'request': request}, many=True)
            return Response(serializer.data)
        ###############################################################
        #검색 관련 로직
        else:
            # 원룸에 대한 정보를 검색하기 위한 URL
            roomRetrieveURL = 'http://127.0.0.1:8000/db/room/' + '?'
            # 주소 정보가 들어왔다면 URL 끝에 해당 정보를 붙인다.
            if data1.get('address'):
                roomRetrieveURL = roomRetrieveURL + 'address=' + data1.get('address')[0]
            # 건축년도에 대한 정보가 들어왔다면 URL 끝에 해당 정보를 붙인다.
            if data1.get('builtFrom'):
                if roomRetrieveURL[-1] != '?':
                    roomRetrieveURL = roomRetrieveURL + '&'
                roomRetrieveURL = roomRetrieveURL + 'builtFrom=' + data1.get('builtFrom')[0]
            if data1.get('builtTo'):
                if roomRetrieveURL[-1] != '?':
                    roomRetrieveURL = roomRetrieveURL + '&'
                roomRetrieveURL = roomRetrieveURL + 'builtTo=' + data1.get('builtTo')[0]
            # 공통 정보에 대한 사항이 들어왔다면 URL 끝에 해당 정보를 붙인다.
            #N = len(CommonInfo.objects.all())
            N=3
            if data1.get('commonInfo'):
                for info in data1.get('commonInfo'):
                    if roomRetrieveURL[-1] != '?':
                        roomRetrieveURL = roomRetrieveURL + '&'
                    roomRetrieveURL = roomRetrieveURL + 'commonInfo=' + info

            # 완성된 URL로 해당하는 원룸들의 정보를 받는다.
            room_data = None
            if roomRetrieveURL[-1] != '?':
                room_data = json.loads(requests.get(roomRetrieveURL).text)
            # 해당하는 원룸들에 대한 리뷰들을 검색하는 쿼리를 만든다.
            if room_data:
                query_room = Q()
                for r in room_data:
                    query_room.add(Q(roomId=r['id']), Q.OR)
                query.add(query_room, Q.AND)

        # 쿼리로 검색한다. 만약 원룸 검색 결과가 아예 없었다면 검색 결과를 None으로 처리한다.
        searched = Review.objects.filter(query)
        # 검색된 값을 반환한다.
        return Response(ReviewSerializer2(searched, many=True).data)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, args, kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        # 리뷰 번호와 일치하는 리뷰 데이터를 가져온다.
        instance = self.get_object()
        # 기존 데이터를 직렬화한다.
        data = self.get_serializer(instance).data
        # 수정할 리뷰의 종류 및 PK 를 획득한다.
        review_kind = data['reviewKind']
        review_id = data['id']
        # 해당 리뷰의 기존 아이콘 데이터를 불러와 삭제한다.
        #for icon in data['icons']:
        #    a=3
            #requests.delete('http://127.0.0.1:8000/db/icon/'+icon.icon_id)
        # 입력받은 데이터를 data1으로 받는다. (data1은 JSON(dictionary) 타입)
        data1 = request.data
        # 텍스트 리뷰인 경우
        if review_kind == 0:
            # 리뷰 본문 데이터를 가져온다.
            review_sentence = data1['reviewSentence']
            # 시각화 모듈을 이용해 리뷰 본문 텍스트로 아이콘 생성 및 저장이 이뤄진다.
            #시각화모듈(reviewSentence)
            # 따라서 본 메소드에서는 해당 과정을 구현하지 않는다.
            # 기존 데이터에서 리뷰 본문만 새 데이터로 변경한다.
            data['reviewSentence']=sentence_spliter(review_sentence)
        # 이미지 리뷰인 경우
        elif review_kind == 1:
            # 리뷰 본문을 생성하기 위한 변수를 선언한다.
            review_sentence = ''
        # 입력받은 데이터들을 확인
            for key in data1:
                # 아이콘 데이터만 dictionary로 들어옴
                if type(data1[key]) is dict:
                    icon = data1[key]
                    # 리뷰 본문의 뒤에 해당 아이콘의 주석을 이어붙인다.
                    review_sentence = review_sentence + icon['iconInformation']
                    # 입력받은 데이터로 새 아이콘을 생성하는 POST 메소드를 수행한다.
                    icon['revId'] = review_id
                    # requests.post('http://127.0.0.1:8000/db/icon/', data=icon)
            # 생성한 리뷰 본문으로 기존 본문을 변경한다.
            data['reviewSentence']=review_sentence
        # 갱신된 데이터로 새 시리얼라이저를 생성한다.
        serializer = self.get_serializer(instance, data=data)
        # 생성된 시리얼라이저의 유효성을 검사한다.
        serializer.is_valid(raise_exception=True)
        # 검사 후, 그 시리얼라이저로 데이터를 갱신한다.
        self.perform_update(serializer)
        # 성공 응답코드를 반환한다.
        return HttpResponse(status=200)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, args, kwargs)


class RoomViewSets(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, args, kwargs)

    def list(self, request, *args, **kwargs):
        # URL의 파라미터들을 사전형 배열로 받는다.
        data1 = dict(request.GET)
        # 별도의 검색조건이 없다면 모델의 모든 값을 반환한다.
        if not data1:
            return super().list(self, request, args, kwargs)
        # 검색 조건으로 기본 쿼리를 만든다.
        query = Q()  # 메인 쿼리로, 최종 결과를 낼 때 사용한다.
        # 주소에 대한 검색을 수행하는 쿼리를 만든다.
        if data1.get('address'):
            query_address = Q()  # 주소에 대한 쿼리이다.
            for ad in data1.get('address'):
                query_address.add(Q(address__contains=ad), Q.OR)
            query.add(query_address, Q.AND)
        # 건축년도에 대한 검색을 수행하는 쿼리를 만든다.
        if data1.get('builtFrom') or data1.get('builtTo'):
            query_built_year = Q()  # 건축년도에 대한 쿼리이다.
            built_from = 0
            built_to = 2023
            if data1.get('builtFrom'):
                built_from = data1.get('builtFrom')[0]
            if data1.get('builtTo'):
                built_to = data1.get('builtTo')[0]
            query_built_year = Q(builtYear__range=(int(built_from), int(built_to)))
            query.add(query_built_year, Q.AND)
        #N = len(CommonInfo.objects.all())
        N = 10
        if data1.get('commonInfo'):
            query_common_info = Q()  # 공통 정보에 대한 쿼리이다.
            for info in data1.get('commonInfo'):   # 입력된 공통 정보 번호를 검색 조건에 추가한다.
                query_common_info.add(Q(commonInfo__contains=(int(info))), Q.AND)
            query.add(query_common_info, Q.AND)

        #최종 검색을 한다.
        searched = Room.objects.filter(query)
        # 검색 결과를 반환한다.
        return Response(self.get_serializer(searched, many=True).data)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        # URL의 lookup 필드에 해당하는 값으로 모델에서 인스턴스를 꺼낸다.
        instance = self.get_object()
        # 인스턴스의 값들을 해당하는 모델에 대한 시리얼라이저로 직렬화한다.
        data1 = self.get_serializer(instance).data
        # request로 받은 데이터를 dictionary 값으로 변수에 넣는다.
        data2 = dict(request.data)
        # data1에서 입력받은 값들만 변환한다.
        for key in data2:
            if data2[key] != '':
                data1[key] = data2[key][0] # (입력받은 값들은['']의 형태로 배열로 들어온다.)
        # 갱신된 인스턴스를 직렬화한다.
        serializer = self.get_serializer(instance, data=data1)
        # 시리얼라이저의 유효 여부를 검사한다.
        serializer.is_valid(raise_exception=True)
        # 모델에 갱신된 인스턴스 정보를 저장한다.
        self.perform_update(serializer)
        # 갱신이 성공했음을 반환한다.
        return Response("Update Success!")

    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, args, kwargs)


class IconViewSets(ModelViewSet):
    queryset = Icon.objects.all()
    serializer_class = IconSerializer

    def update(self, request, *args, **kwargs):
        # URL의 lookup 필드에 해당하는 값으로 모델에서 인스턴스를 꺼낸다.
        instance = self.get_object()
        # 인스턴스의 값들을 해당하는 모델에 대한 시리얼라이저로 직렬화한다.
        data1 = self.get_serializer(instance).data
        # request로 받은 데이터를 dictionary 값으로 변수에 넣는다.
        data2 = dict(request.data)
        # data1에서 입력받은 값들만 변환한다.
        for key in data2:
            if data2[key] != '':
                data1[key] = data2[key][0] # (입력받은 값들은['']의 형태로 배열로 들어온다.)
        # 갱신된 인스턴스를 직렬화한다.
        serializer = self.get_serializer(instance, data=data1)
        # 시리얼라이저의 유효 여부를 검사한다.
        serializer.is_valid(raise_exception=True)
        # 모델에 갱신된 인스턴스 정보를 저장한다.
        self.perform_update(serializer)
        # 갱신이 성공했음을 반환한다.
        return Response("Update Success!")


class RecommendViewSets(ModelViewSet):
    queryset = Recommend.objects.all()
    serializer_class = RecommendSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        print(serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        # URL의 파라미터들을 사전형 배열로 받는다.
        data1 = dict(request.GET)
        # 별도의 검색조건이 없다면 모델의 모든 값을 반환한다.
        if not data1:
            return super().list(self, request, args, kwargs)
        if data1.get('reviewId') and data1.get('uId'):
            f = Q(uId= data1.get('uId')[0])
            f.add(Q(reviewId= int(data1.get('reviewId')[0])), Q.AND)
            result = Recommend.objects.filter(f)
            return Response(result[0].id)

    def update(self, request, *args, **kwargs):
        # URL의 lookup 필드에 해당하는 값으로 모델에서 인스턴스를 꺼낸다.
        instance = self.get_object()
        # 인스턴스의 값들을 해당하는 모델에 대한 시리얼라이저로 직렬화한다.
        data1 = self.get_serializer(instance).data
        # request로 받은 데이터를 dictionary 값으로 변수에 넣는다.
        data2 = dict(request.data)
        # data1에서 입력받은 값들만 변환한다.
        for key in data2:
            if data2[key] != '':
                data1[key] = data2[key][0] # (입력받은 값들은['']의 형태로 배열로 들어온다.)
        # 갱신된 인스턴스를 직렬화한다.
        serializer = self.get_serializer(instance, data=data1)
        # 시리얼라이저의 유효 여부를 검사한다.
        serializer.is_valid(raise_exception=True)
        # 모델에 갱신된 인스턴스 정보를 저장한다.
        self.perform_update(serializer)
        # 갱신이 성공했음을 반환한다.
        return Response("Update Success!")


class ReportViewSets(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def list(self, request, *args, **kwargs):
        # URL의 파라미터들을 사전형 배열로 받는다.
        data1 = dict(request.GET)
        # 별도의 검색조건이 없다면 모델의 모든 값을 반환한다.
        if not data1:
            return super().list(self, request, args, kwargs)
        if data1.get('reviewId') and data1.get('uId'):
            f = Q(uId= data1.get('uId')[0])
            f.add(Q(reviewId= int(data1.get('reviewId')[0])), Q.AND)
            result = Report.objects.filter(f)
            return Response(result[0].id)

    def update(self, request, *args, **kwargs):
        # URL의 lookup 필드에 해당하는 값으로 모델에서 인스턴스를 꺼낸다.
        instance = self.get_object()
        # 인스턴스의 값들을 해당하는 모델에 대한 시리얼라이저로 직렬화한다.
        data1 = self.get_serializer(instance).data
        # request로 받은 데이터를 dictionary 값으로 변수에 넣는다.
        data2 = dict(request.data)
        # data1에서 입력받은 값들만 변환한다.
        for key in data2:
            if data2[key] != '':
                data1[key] = data2[key][0] # (입력받은 값들은['']의 형태로 배열로 들어온다.)
        # 갱신된 인스턴스를 직렬화한다.
        serializer = self.get_serializer(instance, data=data1)
        # 시리얼라이저의 유효 여부를 검사한다.
        serializer.is_valid(raise_exception=True)
        # 모델에 갱신된 인스턴스 정보를 저장한다.
        self.perform_update(serializer)
        # 갱신이 성공했음을 반환한다.
        return Response("Update Success!")

    def destroy(self, request, *args, **kwargs):
        # lookup 필드를 통해 해당하는 신고 인스턴스 획득
        instance = self.get_object()
        # 시리얼라이저로 인스턴스를 직렬화()
        data = self.get_serializer(instance).data
        # 관리자 여부 확인
        if not request.user.is_staff:
            return super().destroy(self, request, args, kwargs)
        # 신고를 작성한 회원의 회원번호를 구함
        u_id = data['uId']
        # 해당 회원의 retrieve 메소드를 HTTP GET 메소드를 이용하여 획득
        user = json.loads(requests.get('http://127.0.0.1:8000/db/user/' + str(u_id) + '/').text)
        # 회원의 경고 횟수를 1 증가
        user['uWarnCount'] = user['uWarnCount'] + 1
        # 경고 횟수에 따라서 상태 변경
        if user['uWarnCount'] == 20:
            user['uActive'] = 4
            user['penaltyDate'] = datetime.date.today
        elif user['uWarnCount'] >= 15:
            user['uActive'] = 3
            user['penaltyDate'] = datetime.date.today
        elif user['uWarnCount'] >= 10:
            user['uActive'] = 2
            user['penaltyDate'] = datetime.date.today
        elif user['uWarnCount'] >= 5:
            user['uActive'] = 1
        # 회원 정보 update
        requests.put('http://127.0.0.1:8000/db/user/' + str(u_id) + '/', data=user)
        # 신고 데이터 삭제
        return super().destroy(self, request, args, kwargs)


class CommonInfoViewSets(ModelViewSet):
    queryset = CommonInfo.objects.all()
    serializer_class = CommonInfoSerializer

    def update(self, request, *args, **kwargs):
        # URL의 lookup 필드에 해당하는 값으로 모델에서 인스턴스를 꺼낸다.
        instance = self.get_object()
        # 인스턴스의 값들을 해당하는 모델에 대한 시리얼라이저로 직렬화한다.
        data1 = self.get_serializer(instance).data
        # request로 받은 데이터를 dictionary 값으로 변수에 넣는다.
        data2 = dict(request.data)
        # data1에서 입력받은 값들만 변환한다.
        for key in data2:
            if data2[key] != '':
                data1[key] = data2[key][0] # (입력받은 값들은['']의 형태로 배열로 들어온다.)
        # 갱신된 인스턴스를 직렬화한다.
        serializer = self.get_serializer(instance, data=data1)
        # 시리얼라이저의 유효 여부를 검사한다.
        serializer.is_valid(raise_exception=True)
        # 모델에 갱신된 인스턴스 정보를 저장한다.
        self.perform_update(serializer)
        # 갱신이 성공했음을 반환한다.
        return Response("Update Success!")


class ImageViewSets(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def update(self, request, *args, **kwargs):
        # URL의 lookup 필드에 해당하는 값으로 모델에서 인스턴스를 꺼낸다.
        instance = self.get_object()
        # 인스턴스의 값들을 해당하는 모델에 대한 시리얼라이저로 직렬화한다.
        data1 = self.get_serializer(instance).data
        # request로 받은 데이터를 dictionary 값으로 변수에 넣는다.
        data2 = dict(request.data)
        # data1에서 입력받은 값들만 변환한다.
        for key in data2:
            if data2[key] != '':
                data1[key] = data2[key][0] # (입력받은 값들은['']의 형태로 배열로 들어온다.)
        # 갱신된 인스턴스를 직렬화한다.
        serializer = self.get_serializer(instance, data=data1)
        # 시리얼라이저의 유효 여부를 검사한다.
        serializer.is_valid(raise_exception=True)
        # 모델에 갱신된 인스턴스 정보를 저장한다.
        self.perform_update(serializer)
        # 갱신이 성공했음을 반환한다.
        return Response("Update Success!")


def ajaxTest(request):
    manager = json.loads(requests.get('http://127.0.0.1:8000/db/manager/').text)
    print(manager)
    return render(request, 'test.html', {"manager": manager})
