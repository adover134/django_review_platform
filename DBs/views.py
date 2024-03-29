from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.shortcuts import render
from django.db.models import Q, Count

import datetime

import requests
import json
import copy
from DBs.serializers import UserSerializer, ReviewSerializer, RoomSerializer, IconSerializer, RecommendSerializer, ReportSerializer, ReviewImageSerializer, RoomImageSerializer, ReviewSerializerLink
from DBs.models import User, Review, Room, Icon, Recommend, Report, ReviewImage, RoomImage
from DBs.services import sentence_split, review_to_icons


class UserViewSets(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ReviewViewSets(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        # 입력값을 data로 저장한다.
        data = copy.deepcopy(request.data)
        # 입력값 중 아이콘에 대한 것을 제외하고 data1으로 저장한다.
        data1 = {}
        data1['reviewTitle'] = data.get('reviewTitle')
        data1['roomId'] = int(data.get('roomId'))
        data1['uId'] = int(data.get('uId'))
        data1['rent'] = int(data.get('rent'))
        data1['deposit'] = int(data.get('deposit'))
        if data1['rent'] == 1:
            data1['monthlyRent'] = int(data.get('monthlyRent'))
        data1['roomSize'] = float(data.get('roomSize'))
        data1['soundproof'] = int(data.get('proof'))
        data1['lighting'] = int(data.get('sunshine'))
        data1['cleanliness'] = int(data.get('clean'))
        data1['humidity'] = int(data.get('humidity'))

        s = review_to_icons(data.get('reviewSentence'))

        data1['reviewSentence'] = s['reviews']
        # 시각화 모듈 이용해 리뷰 본문 텍스트로 아이콘 생성 및 저장한다.
        # 시각화모듈(data['reviewSentence'])
        # 완성된 리뷰 정보를 시리얼라이저로 직렬화한다.
        serializer = self.get_serializer(data=data1)
        # 시리얼라이저가 유효하면 저장한다.
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        headers = self.get_success_headers(serializer.data)
        review_id = review.id

        for i in range(len(s['kind'])):
            iconData = {}
            iconData['review'] = s['reviews'][i]
            iconData['kind'] = s['kind'][i]
            iconData['reviewId'] = review_id
            if s['kind'][i] != 4:
                requests.post('http://127.0.0.1:8000/db/icon/', data=iconData)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        # URL의 파라미터들을 사전형 배열로 받는다.
        data1 = dict(request.GET)
        # 별도의 검색조건이 없다면 모델의 모든 값을 반환한다.
        if not data1:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = ReviewSerializer(page, context={'request': request}, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = ReviewSerializer(queryset, context={'request': request}, many=True)
            return Response(serializer.data)
        # 검색 조건을 쿼리로 만들어 저장할 변수와 검색 결과를 저장할 변수를 만든다.
        query = Q()
        searched = None

        # 회원 번호를 받았다면 해당하는 회원의 리뷰만 찾는 쿼리를 만들어 최종 쿼리에 더한다.
        if data1.get('uId'):
            u = data1.get('uId')[0].replace('/', '')
            query_user = Q(uId=u)
            query.add(query_user, Q.AND)
        elif data1.get('roomId'):
            rId = data1.get('roomId')[0]
            rId = rId.replace('/', '')
            query_roomId = Q(roomId_id=rId)
            query.add(query_roomId, Q.AND)
        else:
            # 작성일의 시작점과 끝점을 받았다면 해당 기간 동안 작성된 리뷰만 찾는 쿼리를 만들어 최종 쿼리에 더한다.
            if data1.get('date'):
                date_value = data1.get('date')[0]
                date_value = date_value.replace('/', '')
                today = datetime.date.today()
                from_date = None

                match date_value:
                    case '1week':
                        from_date = today - datetime.timedelta(days=6)
                    case '2weeks':
                        from_date = today - datetime.timedelta(days=13)
                    case '1month':
                        from_date = today - datetime.timedelta(days=30)
                    case '':
                        from_date = today - datetime.timedelta(days=364)

                query_date = Q(reviewDate__range=[from_date, today])
                query.add(query_date, Q.AND)
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
            # 주소 정보가 들어왔다면 해당 주소의 원룸에 대한 리뷰들만 찾는 쿼리를 만든다.
            if data1.get('address'):
                query_room = Q()
                query_room.add(Q(roomId__address__contains=str(data1.get('address')[0])), Q.AND)
                query.add(query_room, Q.AND)
            if data1.get('humidity_from') or data1.get('humidity_to'):
                query_humidity = Q()  # 건축년도에 대한 쿼리이다.
                humidity_from = 1
                humidity_to = 5
                if data1.get('humidity_from'):
                    humidity_from = data1.get('humidity_from')[0]
                if data1.get('humidity_to'):
                    humidity_to = data1.get('humidity_to')[0]
                query_humidity = Q(humidity__range=(int(humidity_from), int(humidity_to)))
                query.add(query_humidity, Q.AND)
            if data1.get('soundproof_from') or data1.get('soundproof_to'):
                query_soundproof = Q()  # 건축년도에 대한 쿼리이다.
                soundproof_from = 0
                soundproof_to = 2023
                if data1.get('soundproof_from'):
                    soundproof_from = data1.get('soundproof_from')[0]
                if data1.get('soundproof_to'):
                    soundproof_to = data1.get('soundproof_to')[0]
                query_soundproof = Q(soundproof__range=(int(soundproof_from), int(soundproof_to)))
                query.add(query_soundproof, Q.AND)
            if data1.get('lighting_from') or data1.get('lighting_to'):
                query_lighting = Q()  # 건축년도에 대한 쿼리이다.
                lighting_from = 0
                lighting_to = 2023
                if data1.get('lighting_from'):
                    lighting_from = data1.get('lighting_from')[0]
                if data1.get('lighting_to'):
                    lighting_to = data1.get('lighting_to')[0]
                query_lighting = Q(lighting__range=(int(lighting_from), int(lighting_to)))
                query.add(query_lighting, Q.AND)
            if data1.get('cleanliness_from') or data1.get('builtTo'):
                query_cleanliness = Q()  # 건축년도에 대한 쿼리이다.
                cleanliness_from = 0
                cleanliness_to = 2023
                if data1.get('cleanliness_from'):
                    cleanliness_from = data1.get('cleanliness_from')[0]
                if data1.get('cleanliness_to'):
                    cleanliness_to = data1.get('cleanliness_to')[0]
                query_cleanliness = Q(cleanliness__range=(int(cleanliness_from), int(cleanliness_to)))
                query.add(query_cleanliness, Q.AND)

        # 쿼리로 검색한다. 만약 원룸 검색 결과가 아예 없었다면 검색 결과를 None으로 처리한다.
        # 위의 로직에서 원룸 데이터에 대한 검색조건이 query_room에 담긴다.
        # 그다음에는 해당하는 원룸 ID로 Review.obects.filter()를 써야한다.
        if query == Q():
            searched = None
        else:
            searched = Review.objects.filter(query)
            if data1.get('icons'):
                searched = (
                    searched.filter(includedIcon__iconKind__in=data1.get('icons')).annotate(total=Count('id')).order_by(
                        'total')).filter(total=len(data1.get('icons')))
            # 정렬조건
            if data1.get('sorted'):
                sort_value = data1.get('sorted')[0]
                sort_value = sort_value.replace('/', '')

                match sort_value:
                    case '1': # 최신순
                        searched = searched.order_by('reviewDate')
                    case '2': # 추천순
                        searched = searched.annotate(recommend_count=Count('recommendedOn')).order_by('-recommend_count')
                    case '3': # 정확도순(아이콘 많은 순)
                        searched = searched.annotate(includedIcon_count=Count('includedIcon')).order_by('-includedIcon_count')
        print(searched)
        # 검색된 값을 반환한다.
        return Response(ReviewSerializer(searched, many=True, context={'request': request}).data)


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ReviewSerializerLink(instance, context={'request': request})
        return Response(serializer.data)


    def update(self, request, *args, **kwargs):
        # 리뷰 번호와 일치하는 리뷰 데이터를 가져온다.
        instance = self.get_object()
        # 기존 데이터를 직렬화한다.
        data = ReviewSerializerLink(instance, context={'request': request}).data
        print(data.get('includedIcon'))
        for i in data.get('includedIcon'):
            requests.delete(i)
        # 수정할 리뷰의 PK 를 획득한다.
        review_id = data['id']
        update_data = copy.deepcopy(request.data)
        data['reviewTitle'] = update_data.get('reviewTitle')
        data['roomId'] = int(update_data.get('roomId'))
        data['uId'] = int(update_data.get('uId'))
        data['rent'] = int(update_data.get('rent'))
        data['deposit'] = int(update_data.get('deposit'))
        if update_data.get('monthlyRent'):
            data['monthlyRent'] = int(update_data.get('monthlyRent'))
        data['roomSize'] = float(update_data.get('roomSize'))
        data['soundproof'] = int(update_data.get('proof'))
        data['lighting'] = int(update_data.get('sunshine'))
        data['cleanliness'] = int(update_data.get('clean'))
        data['humidity'] = int(update_data.get('humidity'))

        review_sentence = review_to_icons(update_data.get('reviewSentence'))
        data['reviewSentence'] = review_sentence['reviews']

        # 새 분석 결과를 아이콘 정보로 저장한다.
        for i in range(len(review_sentence['kind'])):
            iconData = {}
            iconData['review'] = review_sentence['reviews'][i]
            iconData['kind'] = review_sentence['kind'][i]
            iconData['reviewId'] = review_id
            if review_sentence['kind'][i] != 4:
                requests.post('http://127.0.0.1:8000/db/icon/', data=iconData)

        # 갱신된 데이터로 새 시리얼라이저를 생성한다.
        serializer = self.get_serializer(instance, data=data)
        # 생성된 시리얼라이저의 유효성을 검사한다.
        serializer.is_valid(raise_exception=True)
        # 검사 후, 그 시리얼라이저로 데이터를 갱신한다.
        self.perform_update(serializer)
        # 성공 응답코드를 반환한다.
        return Response(serializer.data, status=status.HTTP_200_OK)



class RoomViewSets(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def create(self, request, *args, **kwargs):
        data = dict(copy.deepcopy(request.data))
        data1 = {}
        if data.get('address'):
            if isinstance(data.get('address'), list):
                data1['address'] = data.get('address')[0]
            else:
                data1['address'] = data.get('address')
        elif data.get('room_address'):
            if isinstance(data.get('room_address'), list):
                data1['address'] = data.get('room_address')[0]
            else:
                data1['address'] = data.get('address')
        if isinstance(data.get('postcode'), list) and data.get('postcode') != ['']:
            data1['postcode'] = int(data.get('postcode')[0])
        else:
            data1['postcode'] = int(data.get('postcode'))
        data1['commonInfo'] = []
        if data.get('commonInfo'):
            for index in range(len(data.get('commonInfo'))):
                if data.get('commonInfo')[index] == 'true':
                    data1['commonInfo'].append(index - 1)
        if data.get('name'):
            if isinstance(data.get('name'), list):
                data1['name'] = data.get('name')[0]
            else:
                data1['name'] = data.get('name')
        if data.get('builtYear'):
            if isinstance(data.get('builtYear'), list):
                data1['builtYear'] = data.get('builtYear')[0]
            else:
                data1['builtYear'] = data.get('builtYear')
        if data.get('distance'):
            if isinstance(data.get('distance'), list) and data.get('distance') != ['']:
                data1['distance'] = int(data.get('distance')[0])
            else:
                data1['distance'] = int(data.get('distance'))
        if data.get('convNum'):
            if isinstance(data.get('convNum'), list) and data.get('convNum') != ['']:
                data1['convNum'] = int(data.get('convNum')[0])
            else:
                data1['convNum'] = int(data.get('convNum'))
        if data.get('ownerPhone'):
            if isinstance(data.get('ownerPhone'), list):
                data1['ownerPhone'] = data.get('ownerPhone')[0]
            else:
                data1['ownerPhone'] = data.get('ownerPhone')
        if data.get('buildingFloorNum') and data.get('buildingFloorNum') != ['']:
            if isinstance(data.get('buildingFloorNum'), list):
                data1['buildingFloorNum'] = data.get('buildingFloorNum')[0]
            else:
                data1['buildingFloorNum'] = data.get('buildingFloorNum')
        serializer = self.get_serializer(data=data1)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def list(self, request, *args, **kwargs):
        # URL의 파라미터들을 사전형 배열로 받는다.
        data1 = dict(request.GET)
        # 별도의 검색조건이 없다면 모델의 모든 값을 반환한다.
        if not data1:
            return super().list(self, request, args, kwargs)
        # 검색 조건으로 기본 쿼리를 만든다.
        query = Q()  # 메인 쿼리로, 최종 결과를 낼 때 사용한다.
        if data1.get('full_address'):
            query_full_address = Q()  # 주소에 대한 쿼리이다.
            if isinstance(data1.get('full_address'), list):
                query_full_address.add(Q(address=data1.get('full_address')[0]), Q.OR)
            else:
                query_full_address.add(Q(address=data1.get('full_address')), Q.OR)
            query.add(query_full_address, Q.AND)
        # 주소에 대한 검색을 수행하는 쿼리를 만든다.
        if data1.get('address'):
            query_address = Q()  # 주소에 대한 쿼리이다.
            for ad in data1.get('address'):
                query_address.add(Q(address__contains=ad), Q.OR)
            query.add(query_address, Q.AND)
        # 학교까지의 거리에 대한 검색을 수행하는 쿼리를 만든다.
        if data1.get('distance_from') or data1.get('distance_to'):
            query_distance = Q()  # 건축년도에 대한 쿼리이다.
            distance_from = 1
            distance_to = 10
            if data1.get('distance_from'):
                distance_from = data1.get('distance_from')[0]
            if data1.get('distance_to'):
                distance_to = data1.get('distance_to')[0]
            query_distance = Q(distance__range=(int(distance_from), int(distance_to)))
            query.add(query_distance, Q.AND)
        # 반경 300미터 이내의 편의점 수에 대한 검색을 수행하는 쿼리를 만든다.
        if data1.get('distance_from') or data1.get('distance_to'):
            query_convNum = Q()  # 건축년도에 대한 쿼리이다.
            convNum_from = 1
            convNum_to = 10
            if data1.get('convNum_from'):
                convNum_from = data1.get('convNum_from')[0]
            if data1.get('convNum_to'):
                convNum_to = data1.get('convNum_to')[0]
            query_convNum = Q(convNum__range=(int(convNum_from), int(convNum_to)))
            query.add(query_convNum, Q.AND)
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
        if data1.get('commonInfo'):
            query_common_info = Q()  # 공통 정보에 대한 쿼리이다.
            for info in data1.get('commonInfo'):  # 입력된 공통 정보 번호를 검색 조건에 추가한다.
                query_common_info.add(Q(commonInfo__contains=(int(info))), Q.AND)
            query.add(query_common_info, Q.AND)
        if data1.get('postcode'):
            query_postcode = Q()
            postcode = data1.get('postcode')[0]
            postcode = postcode.replace('/', '')
            query_postcode = Q(postcode=postcode)
            query.add(query_postcode, Q.AND)
        # 최종 검색을 한다.
        searched = Room.objects.filter(query)
        # 검색 결과를 반환한다.
        return Response(self.get_serializer(searched, many=True).data)


    def update(self, request, *args, **kwargs):
        # URL의 lookup 필드에 해당하는 값으로 모델에서 인스턴스를 꺼낸다.
        instance = self.get_object()
        # 인스턴스의 값들을 해당하는 모델에 대한 시리얼라이저로 직렬화한다.
        data1 = self.get_serializer(instance).data
        # request로 받은 데이터를 dictionary 값으로 변수에 넣는다.
        data2 = dict(request.data)
        # data1에서 입력받은 값들만 변환한다.

        if data2.get('address'):
            if isinstance(data2.get('address'), list):
                data1['address'] = data2.get('address')[0]
            else:
                data1['address'] = data2.get('address')
        elif data2.get('room_address'):
            if isinstance(data2.get('room_address'), list):
                data1['address'] = data2.get('room_address')[0]
            else:
                data1['address'] = data2.get('address')
        if isinstance(data2.get('postcode'), list):
            data1['postcode'] = int(data2.get('postcode')[0])
        else:
            data1['postcode'] = int(data2.get('postcode'))
        data1['commonInfo'] = []
        if data2.get('commonInfo'):
            for index in range(len(data2.get('commonInfo'))):
                if data2.get('commonInfo')[index] == 'true':
                    data1['commonInfo'].append(index - 1)
        if data2.get('name'):
            if isinstance(data2.get('name'), list):
                data1['name'] = data2.get('name')[0]
            else:
                data1['name'] = data2.get('name')
        if data2.get('builtYear' and data2.get('builtYear') != ['']):
            if isinstance(data2.get('builtYear'), list):
                data1['builtYear'] = data2.get('builtYear')[0]
            else:
                data1['builtYear'] = data2.get('builtYear')
        if data2.get('ownerPhone'):
            if isinstance(data2.get('ownerPhone'), list):
                data1['ownerPhone'] = data2.get('ownerPhone')[0]
            else:
                data1['ownerPhone'] = data2.get('ownerPhone')
        if isinstance(data2.get('distance'), list) and data2.get('distance') != ['']:
            data1['distance'] = int(data2.get('distance')[0])
        else:
            data1['distance'] = int(data2.get('distance'))
        if data2.get('buildingFloorNum') and data2.get('buildingFloorNum') != ['']:
            if isinstance(data2.get('buildingFloorNum'), list):
                data1['buildingFloorNum'] = data2.get('buildingFloorNum')[0]
            else:
                data1['buildingFloorNum'] = data2.get('buildingFloorNum')
        # 갱신된 인스턴스를 직렬화한다.
        serializer = self.get_serializer(instance, data=data1)
        # 시리얼라이저의 유효 여부를 검사한다.
        serializer.is_valid(raise_exception=True)
        # 모델에 갱신된 인스턴스 정보를 저장한다.
        self.perform_update(serializer)
        # 갱신이 성공했음을 반환한다.
        return Response(serializer.data)



class IconViewSets(ModelViewSet):
    queryset = Icon.objects.all()
    serializer_class = IconSerializer


    def create(self, request, *args, **kwargs):
        # 입력값을 data로 저장한다.
        data = copy.deepcopy(request.data)
        data1 = {}
        if isinstance(data.get('reviewId'), str):
            data1['reviewId'] = data.get('reviewId')
        else:
            data1['reviewId'] = data.get('reviewId')[0]
        if data.get('kind'):
            match(data['kind'][0]):
                case '0': # 교통 정보 아이콘 이름
                    data1['iconKind'] = '0'
                    data1['changedIconKind'] = '00'
                case '1': # 주변 정보 아이콘 이름
                    data1['iconKind'] = '1'
                    data1['changedIconKind'] = '11'
                case '2': # 치안 정보 아이콘 이름
                    data1['iconKind'] = '2'
                    data1['changedIconKind'] = '22'
                case '3': # 주거 정보 아이콘 이름
                    data1['iconKind'] = '3'
                    data1['changedIconKind'] = '33'
        else:
            data1['iconKind'] = data['iconKind'][0]
            data1['changedIconKind'] = data['changedIconKind'][0]
        serializer = self.get_serializer(data=data1)
        # 시리얼라이저가 유효하면 저장한다.
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RecommendViewSets(ModelViewSet):
    queryset = Recommend.objects.all()
    serializer_class = RecommendSerializer

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


class ReviewImageViewSets(ModelViewSet):
    queryset = ReviewImage.objects.all()
    serializer_class = ReviewImageSerializer


    def update(self, request, *args, **kwargs):
        # URL의 lookup 필드에 해당하는 값으로 모델에서 인스턴스를 꺼낸다.
        instance = self.get_object()
        # 인스턴스의 값들을 해당하는 모델에 대한 시리얼라이저로 직렬화한다.
        data1 = self.get_serializer(instance).data
        # request로 받은 데이터를 dictionary 값으로 변수에 넣는다.
        data2 = dict(request.data)
        # data1에서, 입력받은 값들만 변환한다.
        for key in data1:
            if data2.get(key):  # 입력받은 값의 키들 중, data1에 있는 키가 있다면 해당 값만 바꿔준다.
                data1[key] = data2[key][0]
        # 갱신된 인스턴스를 직렬화한다.
        serializer = self.get_serializer(instance, data=data1)
        # 시리얼라이저의 유효 여부를 검사한다.
        serializer.is_valid(raise_exception=True)
        # 모델에 갱신된 인스턴스 정보를 저장한다.
        self.perform_update(serializer)
        # 갱신이 성공했음을 반환한다.
        return Response("Update Success!")


class RoomImageViewSets(ModelViewSet):
    queryset = RoomImage.objects.all()
    serializer_class = RoomImageSerializer


    def update(self, request, *args, **kwargs):
        # URL의 lookup 필드에 해당하는 값으로 모델에서 인스턴스를 꺼낸다.
        instance = self.get_object()
        # 인스턴스의 값들을 해당하는 모델에 대한 시리얼라이저로 직렬화한다.
        data1 = self.get_serializer(instance).data
        # request로 받은 데이터를 dictionary 값으로 변수에 넣는다.
        data2 = dict(request.data)
        # data1에서, 입력받은 값들만 변환한다.
        for key in data1:
            if data2.get(key):  # 입력받은 값의 키들 중, data1에 있는 키가 있다면 해당 값만 바꿔준다.
                data1[key] = data2[key][0]
        # 갱신된 인스턴스를 직렬화한다.
        serializer = self.get_serializer(instance, data=data1)
        # 시리얼라이저의 유효 여부를 검사한다.
        serializer.is_valid(raise_exception=True)
        # 모델에 갱신된 인스턴스 정보를 저장한다.
        self.perform_update(serializer)
        # 갱신이 성공했음을 반환한다.
        return Response("Update Success!")


@api_view(['GET'])
def getMainPageReview(request):
    reviews = Review.objects.all()
    latest_data = reviews.order_by('-reviewDate')[:4]
    popular_data = reviews.annotate(recommend_count=Count('recommendedOn')).order_by('-recommend_count')[:4]

    data = {
        'latest_reviews': ReviewSerializer(latest_data, context={'request': request}, many=True).data,
        'popular_reviews': ReviewSerializer(popular_data, context={'request': request}, many=True).data,
    }

    return Response(data)
