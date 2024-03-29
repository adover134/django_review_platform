from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
import requests
import json
import math
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.core.paginator import Paginator
from customForms import customForms
from webPages.config import KAKAO_JAVA_KEY, SOCIAL_AUTH_KAKAO_KEY
from webPages.GeoUtil import GeoUtil


def main(request):
    review_data = json.loads(requests.get('http://127.0.0.1:8000/db/mainPageReviews' + '/').text)
    latest_reviews = review_data.get('latest_reviews')
    latest_icons = []
    for review in latest_reviews:
        latest_icons.append(list(set(list(review.get('includedIcon')))))
    print('werwer', latest_icons)
    popular_reviews = review_data.get('popular_reviews')
    popular_icons = []
    for review in popular_reviews:
        popular_icons.append(list(set(list(review.get('includedIcon')))))
    data = {
        'javakey': KAKAO_JAVA_KEY,
        'latest_reviews': latest_reviews,
        'latest_icons': latest_icons,
        'popular_reviews': popular_reviews,
        'popular_icons': popular_icons,
    }
    return render(request, 'normal_user_main.html', data)


# 로그인 시도 시에 처리되는 메소드
def login(request):
    return render(request, 'normal_user_main.html', {'javakey': KAKAO_JAVA_KEY})


def logout(request):
    auth_logout(request)
    return redirect('/')


def loginPage(request):
    return render(request, 'normal_user_login.html')


def signup(request):
    res = render(request, 'normal_user_main.html', {'javakey': KAKAO_JAVA_KEY})
    return res


@login_required(login_url='/loginPage/')
def infoCheck(request):
    user = request.user
    initial = {
        '성': user.last_name,
        '이름': user.first_name,
        '이메일': user.email
    }
    userForm = customForms.UserInfoForm(initial=initial)

    user_review_url = 'http://127.0.0.1:8000/db/review/?uId=' + str(user.id)

    if 'sorted' in request.GET:
        sorted = request.GET['sorted'] #파라미터로 넘어오는 정렬순을 나타내는 데이터
        user_review_url = user_review_url + '&sorted=' + sorted
    reviews = json.loads(requests.get(user_review_url + '/').text) # 로그인 한 회원이 작성한 리뷰 데이터 목록

    #paginator
    paginator = Paginator(reviews, 5)
    page = request.GET.get('page')
    paged_review = paginator.get_page(page)
    return render(request, 'normal_user_info_check.html', {'userForm': userForm, 'paged_review': paged_review})


def normal_user_review_search(request):
    context = {}

    review_search_url = 'http://127.0.0.1:8000/db/review/?'
    data = dict(request.GET)
    if data.get('address') and data.get('address') != '':
        review_search_url = review_search_url+'address='+data.get('address')[0]
        context['address'] = data.get('address')[0]
    if data.get('icons'):
        context['icons'] = []
        for c in data.get('icons'):
            review_search_url = review_search_url+'&'+'icons='+c
            context['icons'].append([c])
    if data.get('sorted'):
        if review_search_url[-1] != '?':
            review_search_url = review_search_url+'&'
        review_search_url = review_search_url+'sorted='+data.get('sorted')[0]
        context['sorted'] = data.get('sorted')[0]
    if data.get('date') and data.get('date') != '':
        if review_search_url[-1] != '?':
            review_search_url = review_search_url + '&'
        review_search_url = review_search_url + 'date=' + data.get('date')[0]
        context['date'] = data.get('date')[0]
    if data.get('humidity_from') and data.get('humidity_from') != '':
        if review_search_url[-1] != '?':
            review_search_url = review_search_url + '&'
        review_search_url = review_search_url + 'humidity_from=' + data.get('humidity_from')[0]
        context['humidity_from'] = data.get('humidity_from')[0]
    if data.get('humidity_to') and data.get('humidity_to') != '':
        review_search_url = review_search_url + '&'
        review_search_url = review_search_url + 'humidity_to=' + data.get('humidity_to')[0]
        context['humidity_to'] = data.get('humidity_to')[0]
    if data.get('soundproof_from') and data.get('soundproof_from') != '':
        review_search_url = review_search_url + '&'
        review_search_url = review_search_url + 'soundproof_from=' + data.get('soundproof_from')[0]
        context['soundproof_from'] = data.get('soundproof_from')[0]
    if data.get('soundproof_to') and data.get('soundproof_to') != '':
        review_search_url = review_search_url + '&'
        review_search_url = review_search_url + 'soundproof_to=' + data.get('soundproof_to')[0]
        context['soundproof_to'] = data.get('soundproof_to')[0]
    if data.get('lighting_from') and data.get('lighting_from') != '':
        review_search_url = review_search_url + '&'
        review_search_url = review_search_url + 'lighting_from=' + data.get('lighting_from')[0]
        context['lighting_from'] = data.get('lighting_from')[0]
    if data.get('lighting_to') and data.get('lighting_to') != '':
        review_search_url = review_search_url + '&'
        review_search_url = review_search_url + 'lighting_to=' + data.get('lighting_to')[0]
        context['lighting_to'] = data.get('lighting_to')[0]
    if data.get('cleanliness_from') and data.get('cleanliness_from') != '':
        review_search_url = review_search_url + '&'
        review_search_url = review_search_url + 'cleanliness_from=' + data.get('cleanliness_from')[0]
        context['cleanliness_from'] = data.get('cleanliness_from')[0]
    if data.get('cleanliness_to') and data.get('cleanliness_to') != '':
        review_search_url = review_search_url + '&'
        review_search_url = review_search_url + 'cleanliness_to=' + data.get('cleanliness_to')[0]
        context['cleanliness_to'] = data.get('cleanliness_to')[0]
    review_list = json.loads(requests.get(review_search_url).text)
    paginator = Paginator(review_list, 5)
    if data.get('page'):
        if isinstance(data.get('page'), list):
            paged_review = paginator.get_page(data.get('page')[0])
        else:
            paged_review = paginator.get_page(data.get('page'))
    else:
        paged_review = paginator.get_page(1)

    context['paged_review'] = paged_review

    return render(request, 'normal_user_review_search.html', context)


@login_required(login_url='/loginPage/')
def normal_user_review_write_page(request):
    context = {'TextForm': customForms.TextReviewWriteForm}
    if request.GET.get('roomId'):
        room = json.loads(requests.get('http://127.0.0.1:8000/db/room/' + str(request.GET.get('roomId')) + '/').text)
        context['address'] = room.get('address')
        context['postcode'] = room.get('postcode')
    return render(request, 'normal_user_review_write.html', context)


def normal_user_review_read(request):
    user = request.user

    review_num = request.GET.get('id')
    review = json.loads(requests.get('http://127.0.0.1:8000/db/review/'+review_num+'/').text)

    if not review.get('id'):
        return redirect('/normal_user_review_search/')

    room = json.loads(requests.get('http://127.0.0.1:8000/db/room/'+str(review.get('roomId'))+'/').text)
    review['roomName'] = room.get('name')
    review['address'] = room.get('address')
    icon_urls = review.get('includedIcon')

    sorted = ''
    if 'sorted' in request.GET:
        sorted = request.GET.get('sorted')

    # 아이콘 4종류에 대해, 해당하는 리뷰의 번호들을 얻을 수 있다.
    icons = []
    icons.append([])
    icons.append([])
    icons.append([])
    icons.append([])
    if icon_urls:
        for i in range(len(icon_urls)):
            icon = json.loads(requests.get(icon_urls[i]).text)

            match icon.get('iconKind'):
                case '0':
                    icons[0].append(i)
                case '1':
                    icons[1].append(i)
                case '2':
                    icons[2].append(i)
                case '3':
                    icons[3].append(i)

    icon = []
    if icons == [[],[],[],[]]:
        icons = None
        icon = []
    else:
        # 출력할 아이콘 목록
        for i in range(4):
            if len(icons[i]) > 0:
                icon.append(i)

    # 해당 리뷰에 대해 추천한 사람 중 사용자가 있는지 확인
    recommended = None
    reported = None
    recommends = review.get('recommendedOn')
    if recommends:
        for recommend in recommends:
            if json.loads(requests.get(recommend).text).get('uId') == user.id:
                recommended = True
                break
    # 해당 리뷰에 대해 신고한 사람 중 사용자가 있는지 확인
    reports = review.get('reportedOn')
    if reports:
        for report in reports:
            if json.loads(requests.get(report).text).get('uId') == user.id:
                reported = True
                break

    if user.is_anonymous:
        reportable = False
    elif user.uActive == 1 or user.uActive == 2 or user.uActive == 3:
        reportable = False
    else:
        reportable = True

    if user.is_anonymous:
        modifiable = False
    elif user.uActive == 3:
        modifiable = False
    else:
        modifiable = True


    review_writer = json.loads(requests.get('http://127.0.0.1:8000/db/user/'+str(review.get('uId'))+'/').text)
    if user.username == review_writer.get('username'):
        is_writer = 'true'
    else:
        is_writer = 'false'

    reviews = get_reviews_by_roomId(str(review.get('roomId')), sorted)

    paginator = Paginator(reviews, 5)
    if request.GET.get('page'):
        if isinstance(request.GET.get('page'), list):
            paged_review = paginator.get_page(request.GET.get('page')[0])
        else:
            paged_review = paginator.get_page(request.GET.get('page'))
    else:
        paged_review =paginator.get_page(1)

    return render(request, 'normal_user_review_read.html', {'review': review, 'paged_review': paged_review, 'icons': icons, 'is_writer': is_writer, 'reportable': reportable, 'modifiable': modifiable, 'icon': icon, 'recommended': recommended, 'reported': reported})


# 리뷰 수정 페이지 GET
@login_required(login_url='/loginPage/')
def normal_user_review_change(request):
    review_num = request.GET.get('id')
    review = json.loads(requests.get('http://127.0.0.1:8000/db/review/' + review_num + '/').text)
    if not review.get('id'):
        return redirect('/normal_user_review_search/')
    roomId = review['roomId']
    room = json.loads(requests.get('http://127.0.0.1:8000/db/room/' + str(roomId)).text) #해당 원룸 데이터

    images = []
    for img in review.get('additionalImage'):
        images.append(json.loads(requests.get(img).text).get('image'))

    context = {
        'images': images,
        'review': review,
        'room': room
    }

    return render(request, 'normal_user_review_write.html', context)


# 리뷰 수정 등록 PUT
@api_view(['POST'])
def normal_user_review_update(request):
    user = request.user
    review_id = None
    if request.method == 'POST':
        data = dict(request.POST)
        data1 = {}
        form = customForms.TextReviewWriteForm(request.POST, request.FILES)
        data1['reviewSentence'] = data['review_sentence']
        images = request.FILES.getlist('images')
        if form.is_valid():
            data1['reviewTitle'] = data['title']
            # 주소로 원룸을 검색한다.
            room = json.loads(requests.get('http://127.0.0.1:8000/db/room/?address=' + data['address'][0]).text)
            # 원룸 번호를 구한다.
            data1['roomId'] = room[0].get('id')
            data1['uId'] = user.id
            data1['rent'] = int(data['checking'][0])
            data1['deposit'] = int(data['deposit'][0])
            if data1['rent'] == 1:
                data1['monthlyRent'] = int(data['monthly'][0])
            area_kind = data['room_area'][0]
            if area_kind == 'room_area':
                data1['roomSize'] = float(data['area'][0])*3.31
            else:
                data1['roomSize'] = float(data['area'][0])
            data1['proof'] = int(data['proof'][0])
            data1['sunshine'] = int(data['sunshine'][0])
            data1['clean'] = int(data['clean'][0])
            data1['humidity'] = int(data['humidity'][0])
            review = requests.put('http://127.0.0.1:8000/db/review/'+str(request.GET.get('id'))+'/', data=data1)
            review_id = request.GET.get('id')
            exists_image = json.loads(review.text).get('additionalImage')
            updated_images = data.get('image_names')[0]
            # 기존 이미지 중, 수정 페이지에서 지운 것들은 DB에서 삭제
            exists_image_names = []
            for image in exists_image:
                img = json.loads(requests.get(image).text)
                exists_image_names.append(img.get('image')[2:])
                if img.get('image')[2:] not in updated_images:
                    requests.delete(image)

            for image in images:
                img = json.loads(
                    requests.post('http://127.0.0.1:8000/db/reviewImage/', data={'reviewId': review_id}).text)
                img_name = handle_uploaded_file(image, str(review_id), 'reviewImage', image.name)
                requests.put('http://127.0.0.1:8000/db/reviewImage/' + str(img.get('id')) + '/',
                             data={'reviewId': review_id, 'image': img_name})
        return Response(review_id)
    else:
        return status.HTTP_403_FORBIDDEN

# 리뷰 수정 페이지 GET
@login_required(login_url='/loginPage/')
def normal_user_room_change(request):
    roomId = request.GET.get('roomId')
    room = json.loads(requests.get('http://127.0.0.1:8000/db/room/' + str(roomId)).text) #해당 원룸 데이터
    if not room.get('id'):
        return redirect('/normal_user_room_search/')
    images = []
    for img in room.get('roomImage'):
        images.append(json.loads(requests.get(img).text).get('image'))
    context = {
        'images': images,
        'room': room
    }
    return render(request, 'normal_user_room_write.html', context)


# 원룸 수정 POST
@api_view(['POST'])
def normal_user_room_update(request):
    if request.method == 'POST':
        data = dict(request.POST)
        form = customForms.RoomWriteForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')
        if form.is_valid():
            room = json.loads(requests.put('http://127.0.0.1:8000/db/room/'+request.GET.get('roomId')+'/', data=data).text)

            room_id = room.get('id')
            exists_image = room.get('roomImage')

            updated_images = data.get('image_names')[0]
            # 기존 이미지 중, 수정 페이지에서 지운 것들은 DB에서 삭제
            exists_image_names = []
            for image in exists_image:
                img = json.loads(requests.get(image).text)
                exists_image_names.append(img.get('image')[2:])
                if img.get('image')[2:] not in updated_images:
                    requests.delete(image)

            for image in images:
                img = json.loads(
                    requests.post('http://127.0.0.1:8000/db/roomImage/', data={'roomId': room.get('id')}).text)
                img_name = handle_uploaded_file(image, str(room_id), 'roomImage', image.name)
                requests.put('http://127.0.0.1:8000/db/roomImage/' + str(img.get('id')) + '/',
                             data={'reviewId': room.get('id'), 'image': img_name})
            return Response(room_id)
        else:
            return status.HTTP_403_FORBIDDEN



@api_view(['POST'])
@login_required()
def normal_user_review_delete(request):
    if json.loads(requests.get('http://127.0.0.1:8000/db/review/'+request.POST.get('review')).text).get('uId') == request.user.id:
        requests.delete('http://127.0.0.1:8000/db/review/'+request.POST.get('review'))
    return Response('success')


@api_view(['POST'])
def normal_user_review_recommend(request):
    data = dict(request.POST)
    user = request.user
    if user.id:
        # 로그인이 되어 있다면 해당하는 리뷰 번호와 사용자 번호로 추천 내역을 DB에 추가한다.
        if data.get('recommended')[0] == 'false':
            data1 = {'uId': user.id, 'reviewId': int(data.get('review')[0])}
            a = requests.post('http://127.0.0.1:8000/db/recommend/', data=data1)
        else:
            # 리뷰 번호와 사용자 번호로 추천 내역을 찾아서 삭제한다.
            url = 'http://127.0.0.1:8000/db/recommend/?reviewId='+str(data.get('review')[0])+'&uId='+str(user.id)
            a = requests.get(url)
            requests.delete('http://127.0.0.1:8000/db/recommend/'+a.text)
    return Response('success')


@api_view(['POST'])
def normal_user_review_report(request):
    data = dict(request.POST)
    user = request.user
    if user.id:
        # 로그인이 되어 있다면 해당하는 리뷰 번호와 사용자 번호로 추천 내역을 DB에 추가한다.
        if data.get('reported')[0] == 'false':
            data1 = {'uId': user.id, 'reviewId': int(data.get('review')[0])}
            a = requests.post('http://127.0.0.1:8000/db/report/', data=data1)
        else:
            # 리뷰 번호와 사용자 번호로 추천 내역을 찾아서 삭제한다.
            url = 'http://127.0.0.1:8000/db/report/?reviewId='+str(data.get('review')[0])+'&uId='+str(user.id)
            a = requests.get(url)
            requests.delete('http://127.0.0.1:8000/db/report/'+a.text)
    return Response('success')


# 파라미터로 받은 원룸 ID를 가진 리뷰 목록 반환(opt. 정렬조건)
def get_reviews_by_roomId(roomId, sorted): # 파라미터: 원룸 아이디
    reviews = json.loads(requests.get('http://127.0.0.1:8000/db/review/?roomId=' + roomId + '/').text)
    # 파라미터 정렬조건 값 존재시
    if sorted != '':
        reviews = json.loads(requests.get(
            'http://127.0.0.1:8000/db/review/?roomId=' + roomId + '&' +
            'sorted=' + sorted + '/').text)  # 원룸 ID를 가진 리뷰 데이터 정렬한 목록

    return reviews


@login_required(login_url='/loginPage/')
def check_user_reviews(request):
    # 정렬 파라미터 존재 조건
    user = request.user
    if 'sorted' in request.GET:
        sorted = request.GET['sorted'] #파라미터로 넘어오는 정렬순을 나타내는 데이터
        reviews = json.loads(requests.get(
            'http://127.0.0.1:8000/db/review/?uId=' + str(user.id) + '&' + 'sorted=' + sorted + '/').text)  # 로그인 한 회원이 작성한 리뷰 데이터 정렬한 목록
    else:
        reviews = json.loads(requests.get('http://127.0.0.1:8000/db/review/?uId=' + str(user.id) + '/').text)  # 로그인 한 회원이 작성한 리뷰 데이터 목록

    #paginator
    paginator = Paginator(reviews, 5)
    page = request.GET.get('page')
    paged_review = paginator.get_page(page)
    return render(request, 'normal_user_review_list.html', {'reviews': paged_review})


def normal_user_room_read(request):
    roomId = request.GET.get('roomId') #파라미터로 넘어오는 원룸 아이디 데이터
    room = json.loads(requests.get('http://127.0.0.1:8000/db/room/' + str(roomId)).text) #해당 원룸 데이터
    if not room.get('id'):
        return redirect('/normal_user_room_search/')
    sorted = ''

    if 'sorted' in request.GET:
        sorted = request.GET.get('sorted')

    reviews = get_reviews_by_roomId(roomId, sorted)

    paginator = Paginator(reviews, 5)
    page = request.GET.get('page')
    if page:
        paged_review = paginator.get_page(page)
    else:
        paged_review = paginator.get_page(1)

    context = {
        'room': room,
        'paged_review': paged_review,
    }
    return render(request, 'normal_user_room_read.html', context)


def room_search(request):
    context = {}

    room_search_url = 'http://127.0.0.1:8000/db/room/'
    data = dict(request.GET)
    room_search_url = room_search_url+'?'
    if data.get('address') and data.get('address') != '':
        if room_search_url[-1] != '?':
            room_search_url = room_search_url+'&'
        room_search_url = room_search_url+'address='+data.get('address')[0]
        context['address'] = data.get('address')[0]
    if data.get('commonInfo'):
        context['commonInfo'] = []
        for c in data.get('commonInfo'):
            room_search_url = room_search_url + '&' + 'commonInfo=' + c
            context['commonInfo'].append([c])
    if data.get('postcode'):
        if room_search_url[-1] != '?':
            room_search_url = room_search_url+'&'
        room_search_url = room_search_url+'postcode='+data.get('postcode')[0]
        context['postcode'] = data.get('postcode')[0]
    if data.get('distance_from') or data.get('distance_to'):
        if data.get('distance_from'):
            if room_search_url[-1] != '?':
                room_search_url = room_search_url+'&'
            room_search_url = room_search_url+'distance_from='+data.get('distance_from')[0]
            context['distance_from'] = data.get('distance_from')[0]
        if data.get('distance_to'):
            if room_search_url[-1] != '?':
                room_search_url = room_search_url+'&'
            room_search_url = room_search_url+'distance_to='+data.get('distance_to')[0]
            context['distance_to'] = data.get('distance_to')[0]
    if data.get('convNum_from') or data.get('convNum_to'):
        if data.get('convNum_from'):
            if room_search_url[-1] != '?':
                room_search_url = room_search_url+'&'
            room_search_url = room_search_url+'convNum_from='+data.get('convNum_from')[0]
            context['convNum_from'] = data.get('convNum_from')[0]
        if data.get('convNum_to'):
            if room_search_url[-1] != '?':
                room_search_url = room_search_url+'&'
            room_search_url = room_search_url+'convNum_to='+data.get('convNum_to')[0]
            context['convNum_to'] = data.get('convNum_to')[0]
    if data.get('builtFrom') or data.get('builtTo'):
        if data.get('builtFrom'):
            if room_search_url[-1] != '?':
                room_search_url = room_search_url+'&'
            room_search_url = room_search_url+'builtFrom='+data.get('builtFrom')[0]
            context['builtFrom'] = data.get('builtFrom')[0]
        if data.get('builtTo'):
            if room_search_url[-1] != '?':
                room_search_url = room_search_url+'&'
            room_search_url = room_search_url+'builtTo='+data.get('builtTo')[0]
            context['builtTo'] = data.get('builtTo')[0]
    if data.get('sorted'):
        if room_search_url[-1] != '?':
            room_search_url = room_search_url+'&'
        room_search_url = room_search_url+'sorted='+data.get('sorted')[0]
        context['sorted'] = data.get('sorted')[0]
    room_list = json.loads(requests.get(room_search_url).text)
    paginator = Paginator(room_list, 5)
    page = request.GET.get('page')
    paged_room = paginator.get_page(page)
    context['rooms'] = paged_room

    return render(request, 'normal_user_room_search.html', context)


@api_view(['POST'])
def review_write(request):
    user = request.user
    review_id = None
    if request.method == 'POST':
        data = dict(request.POST)
        data1 = {}
        form = customForms.TextReviewWriteForm(request.POST, request.FILES)
        data1['reviewSentence'] = data['review_sentence']
        images = request.FILES.getlist('images')
        cont = {}
        if form.is_valid():
            data1['reviewTitle'] = data['title']
            # 주소로 원룸을 검색한다.
            room = json.loads(requests.get('http://127.0.0.1:8000/db/room/?full_address=' + data.get('address')[0]).text)
            # 원룸 번호를 구한다.
            if len(room) > 0:
                data1['roomId'] = room[0].get('id')
            # 해당 원룸이 없다면 만든다.
            else:
                room_data = {}
                room_data['address'] = str(data.get('address')[0])
                room_data['postcode'] = int(data.get('postcode')[0])

                url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + str(data['address'][0])
                headers = {'Authorization': 'KakaoAK ' + SOCIAL_AUTH_KAKAO_KEY}
                result = json.loads(str(requests.get(url, headers=headers).text))
                room_x = float(result['documents'][0].get('x'))
                room_y = float(result['documents'][0].get('y'))
                url2 = 'https://dapi.kakao.com/v2/local/search/address.json?query=충청북도 청주시 서원구 충대로 1'
                headers = {'Authorization': 'KakaoAK ' + SOCIAL_AUTH_KAKAO_KEY}
                result2 = json.loads(str(requests.get(url2, headers=headers).text))
                school_x = float(result2['documents'][0].get('x'))
                school_y = float(result2['documents'][0].get('y'))
                room_data['distance'] = math.ceil(GeoUtil.get_harversion_distance(school_x, school_y, room_x, room_y)*10)

                url3 = 'https://dapi.kakao.com/v2/local/search/keyword.json'
                params = {'query': '편의점', 'x': room_x, 'y': room_y, 'radius': 200}
                total = requests.get(url3, params=params, headers=headers).json()['documents']
                conv = 0
                for i in range(1, len(total)):
                    if (total[i]['category_name'].find('가정,생활 > 편의점') == 0):
                        conv = conv + 1
                room_data['convNum'] = conv

                room = json.loads(requests.post('http://127.0.0.1:8000/db/room/', data=room_data).text)
                data1['roomId'] = room.get('id')
                cont['room_id'] = room.get('id')
            data1['uId'] = str(user.id)
            data1['rent'] = int(data['checking'][0])
            data1['deposit'] = int(data['deposit'][0])
            if data1['rent'] == 1:
                data1['monthlyRent'] = int(data['monthly'][0])
            area_kind = data['room_area'][0]
            if area_kind == 'room_area':
                data1['roomSize'] = float(data['area'][0])*3.31
            else:
                data1['roomSize'] = float(data['area'][0])
            data1['proof'] = int(data['proof'][0])
            data1['sunshine'] = int(data['sunshine'][0])
            data1['clean'] = int(data['clean'][0])
            data1['humidity'] = int(data['humidity'][0])
            review = requests.post('http://127.0.0.1:8000/db/review/', data=data1)
            review_id = json.loads(review.text).get('id')
            for image in images:
                img = json.loads(
                    requests.post('http://127.0.0.1:8000/db/reviewImage/', data={'reviewId': review_id}).text)
                img_name = handle_uploaded_file(image, str(review_id), 'reviewImage', image.name)
                requests.put('http://127.0.0.1:8000/db/reviewImage/' + str(img.get('id')) + '/',
                             data={'reviewId': review_id, 'image': img_name})
        cont['review_id'] = str(review_id)
        return Response(cont)


def handle_uploaded_file(f, rId,  kind, name):
    with open('static/images/'+kind+'/' + rId + '-' + name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return rId + '-' + name


@login_required(login_url='/loginPage/')
def normal_user_room_write_page(request):
    return render(request, 'normal_user_room_write.html')


@api_view(['POST'])
def normal_user_room_write(request):
    if request.method == 'POST':
        data = dict(request.POST)

        addr = data.get('room_address')[0]
        url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + addr
        headers = {'Authorization': 'KakaoAK '+SOCIAL_AUTH_KAKAO_KEY}
        result = json.loads(str(requests.get(url, headers=headers).text))

        url2 = 'https://dapi.kakao.com/v2/local/search/keyword.json'
        params = {'query': '편의점', 'x': result['documents'][0].get('x'), 'y': result['documents'][0].get('y'), 'radius': 200}
        total = requests.get(url2, params=params, headers=headers).json()['documents']
        conv = 0
        for i in range(1, len(total)):
            if (total[i]['category_name'].find('가정,생활 > 편의점') == 0):
                conv = conv+1
        images = request.FILES.getlist('images')
        form = customForms.RoomWriteForm(request.POST, request.FILES)
        if form.is_valid():
            # 우편번호로 원룸 존재 체크
            # 이미 등록된 원룸인 경우
            data1 = {}
            data1['address'] = data.get('room_address')[0]
            data1['postcode'] = data.get('postcode')[0]
            if data.get('name')[0] != '':
                data1['name'] = data.get('name')[0]
            if data.get('buildingFloorNum')[0] != '':
                data1['buildingFloorNum'] = data.get('buildingFloorNum')[0]
            if data.get('builtYear')[0] != '':
                data1['builtYear'] = data.get('builtYear')[0]
            data1['commonInfo'] = data.get('commonInfo')[0]
            if data.get('ownerPhone')[0] != '':
                data1['ownerPhone'] = data.get('ownerPhone')[0]
            if data.get('distance')[0] != '':
                data1['distance'] = data.get('distance')[0]
            data1['convNum'] = conv

            room = json.loads(requests.get('http://127.0.0.1:8000/db/room/?full_address=' + data.get('room_address')[0]).text)
            if room:
                return Response(room[0].get('id')) # 해당 원룸번호 리턴
            else: #등록되지 않은 원룸의 경우 생성
                room = requests.post('http://127.0.0.1:8000/db/room/', data=data1)
                room_id = json.loads(room.text).get('id')
                for image in images:
                    img = json.loads(
                        requests.post('http://127.0.0.1:8000/db/roomImage/', data={'roomId': room_id}).text)
                    img_name = handle_uploaded_file(image, str(room_id), 'roomImage', image.name)
                    requests.put('http://127.0.0.1:8000/db/roomImage/' + str(img.get('id')) + '/',
                                 data={'reviewId': room_id, 'image': img_name})
                return Response(str(room_id))
        else:
            return status.HTTP_403_FORBIDDEN


def introduction(request):
    return render(request, 'introduction.html')


# 회원 탈퇴
# is_active 필드값 1 -> 0으로 변경
@api_view(['PUT'])
def user_inactivated(request):
    user = request.user
    user_data = json.loads(requests.get('http://127.0.0.1:8000/db/user/' + str(user.id) + '/').text)
    user_data['is_active'] = False # 상태 비활성화

    response = requests.put('http://127.0.0.1:8000/db/user/' + str(user.id) + '/', data=user_data)

    return Response('success')
