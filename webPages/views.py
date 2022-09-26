from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
import requests
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.core.paginator import Paginator
from customForms import reviewWriteForms
from webPages.config import KAKAO_JAVA_KEY


def main(request):
    review_data = json.loads(requests.get('http://127.0.0.1:8000/db/mainPageReviews' + '/').text)

    data = {
        'javakey': KAKAO_JAVA_KEY,
        'latest_reviews': review_data.get('latest_reviews'),
        'popular_reviews': review_data.get('popular_reviews'),
    }
    print(data.get('popular_reviews'))
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
    userForm = reviewWriteForms.UserInfoForm(initial={'성': user.last_name, '이름': user.first_name, '이메일': user.email, '경고횟수': user.uWarnCount})
    if 'sorted' in request.GET:
        sorted = request.GET['sorted'] #파라미터로 넘어오는 정렬순을 나타내는 데이터
        print('sorted = ', sorted)
        reviews = json.loads(requests.get(
            'http://127.0.0.1:8000/db/review/?uId=' + str(user.id) + '&' + 'sorted=' + sorted + '/').text)  # 로그인 한 회원이 작성한 리뷰 데이터 정렬한 목록
    else:
        reviews = json.loads(requests.get('http://127.0.0.1:8000/db/review/?uId=' + str(user.id) + '/').text) # 로그인 한 회원이 작성한 리뷰 데이터 목록

    #paginator
    paginator = Paginator(reviews, 5)
    page = request.GET.get('page')
    paged_review = paginator.get_page(page)
    return render(request, 'normal_user_info_check.html', {'userForm': userForm, 'reviews': reviews})


def normal_user_review_search(request):
    review_search_url = 'http://127.0.0.1:8000/db/review/'
    data = dict(request.GET)
    review_search_url = review_search_url+'?'
    if data.get('builtFrom'):
        review_search_url = review_search_url+'builtFrom='+data.get('builtFrom')[0]
    if data.get('builtTo'):
        if review_search_url[-1] != '?':
            review_search_url = review_search_url+'&'
        review_search_url = review_search_url+'builtTo='+data.get('builtTo')[0]
    if data.get('address'):
        if review_search_url[-1] != '?':
            review_search_url = review_search_url+'&'
        review_search_url = review_search_url+'address='+data.get('address')[0]
    for i in range(3):
        if data.get('icons'):
            for c in data.get('icons'):
                review_search_url = review_search_url+'&'+'commonInfo='+c
    review_list = json.loads(requests.get(review_search_url).text)
    paginator = Paginator(review_list, 5)
    page = request.GET.get('page')
    paged_review = paginator.get_page(page)
    # print('a:', paged_review[2])
    context = {'paged_review': paged_review}
    return render(request, 'normal_user_review_search.html', context)


@login_required(login_url='/loginPage/')
def normal_user_review_write_page(request):
    form = {'TextForm': reviewWriteForms.TextReviewWriteForm}

    return render(request, 'normal_user_review_write.html', form)


def normal_user_review_read(request):
    user = request.user
    review = None
    review_num = request.GET.get('id')
    review = json.loads(requests.get('http://127.0.0.1:8000/db/review/'+review_num+'/').text)
    address = json.loads(requests.get('http://127.0.0.1:8000/db/room/'+str(review.get('roomId'))+'/').text).get('address')
    review['address'] = address
    icon_urls = review.get('includedIcon')
    icons = []
    if icon_urls:
        for icon in icon_urls:
            icon_info = json.loads(requests.get(icon).text)
            icon_info['iconKind'] = 'images/iconImage/'+icon_info.get('iconKind')+'.png'
            icon_info['changedIconKind'] = 'images/iconImage/' + icon_info.get('changedIconKind') + '.png'
            icons.append(icon_info)
    if user.id:
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
        return render(request, 'normal_user_review_read.html', {'review': review, 'icons': icons, 'alive': 'true', 'user': user, 'recommended': recommended, 'reported': reported})
    else:
        return render(request, 'normal_user_review_read.html', {'review': review, 'icons': icons, 'alive': 'false'})


@api_view(['POST'])
def normal_user_review_recommend(request):
    data = dict(request.POST)
    user = request.user
    if user.id:
        # 로그인이 되어 있다면 해당하는 리뷰 번호와 사용자 번호로 추천 내역을 DB에 추가한다.
        if data.get('recommended')[0] == 'false':
            data1 = {'uId': user.id, 'reviewId': int(data.get('review')[0])}
            print(data1)
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
            print(data1)
            a = requests.post('http://127.0.0.1:8000/db/report/', data=data1)
        else:
            # 리뷰 번호와 사용자 번호로 추천 내역을 찾아서 삭제한다.
            url = 'http://127.0.0.1:8000/db/report/?reviewId='+str(data.get('review')[0])+'&uId='+str(user.id)
            a = requests.get(url)
            print(a.text)
            requests.delete('http://127.0.0.1:8000/db/report/'+a.text)
    return Response('success')


# 특정 원룸 클릭시 리뷰목록과 함께 나오는 페이지
def room_with_reviews_display(request):
    roomId = request.GET['roomId'] #파라미터로 넘어오는 원룸 아이디 데이터
    room = json.loads(requests.get('http://127.0.0.1:8000/db/room/' + str(roomId)).text) #해당 원룸 데이터

    # 정렬 파라미터 존재 조건
    if 'sorted' in request.GET:
        sorted = request.GET['sorted'] #파라미터로 넘어오는 정렬순을 나타내는 데이터
        print('sorted = ', sorted)
        reviews = json.loads(requests.get(
            'http://127.0.0.1:8000/db/review/?roomId=' + roomId + '&' + 'sorted=' + sorted + '/').text)  # 원룸 ID를 가진 리뷰 데이터 정렬한 목록

    else:
        reviews = json.loads(requests.get('http://127.0.0.1:8000/db/review/?roomId=' + roomId + '/').text) #원룸 ID를 가진 리뷰 데이터 목록

    #paginator
    paginator = Paginator(reviews, 5)
    page = request.GET.get('page')
    paged_review = None
    if page:
        paged_review = paginator.get_page(page)
    else:
        paged_review = paginator.get_page(1)

    data = {
        'room': room,
        'reviews': paged_review,
    }
    print(data['reviews'][0])

    return render(request, 'room_test.html', data)


@login_required(login_url='/loginPage/')
def change_user_info(request):
    user = request.user
    if request.method == 'POST':
        data = dict(request.POST)
        print(data)
        data1 = {'first_name': data.get('이름'), 'last_name': data.get('성'), 'email': data.get('이메일'), 'layout': data.get('레이아웃')}
        requests.put('http://localhost:8000/db/user/'+str(user.id)+'/', data=data1)

    return render(request, 'normal_user_info_check.html')


@login_required(login_url='/loginPage/')
def check_user_reviews(request):
    # 정렬 파라미터 존재 조건
    user = request.user
    if 'sorted' in request.GET:
        sorted = request.GET['sorted'] #파라미터로 넘어오는 정렬순을 나타내는 데이터
        reviews = json.loads(requests.get(
            'http://127.0.0.1:8000/db/review/?uId=' + str(user.id) + '&' + 'sorted=' + sorted + '/').text)  # 로그인 한 회원이 작성한 리뷰 데이터 정렬한 목록
    else:
        reviews = json.loads(requests.get('http://127.0.0.1:8000/db/review/?uId=' + str(user.id) + '/').text) # 로그인 한 회원이 작성한 리뷰 데이터 목록

    #paginator
    paginator = Paginator(reviews, 5)
    page = request.GET.get('page')
    paged_review = paginator.get_page(page)
    print(paged_review[0])
    return render(request, 'normal_user_review_list.html', {'reviews': paged_review})


def room_test(request):
    roomId = request.GET['roomId'] #파라미터로 넘어오는 원룸 아이디 데이터
    room = json.loads(requests.get('http://127.0.0.1:8000/db/room/' + str(roomId)).text) #해당 원룸 데이터

    # 정렬 파라미터 존재 조건
    if 'sorted' in request.GET:
        sorted = request.GET['sorted'] #파라미터로 넘어오는 정렬순을 나타내는 데이터
        print('sorted = ', sorted)
        reviews = json.loads(requests.get(
            'http://127.0.0.1:8000/db/review/?roomId=' + roomId + '&' + 'sorted=' + sorted + '/').text)  # 원룸 ID를 가진 리뷰 데이터 정렬한 목록

    else:
        reviews = json.loads(requests.get('http://127.0.0.1:8000/db/review/?roomId=' + roomId + '/').text) #원룸 ID를 가진 리뷰 데이터 목록

    #paginator
    paginator = Paginator(reviews, 5)
    page = request.GET.get('page')
    if page:
        paged_review = paginator.get_page(page)
    else:
        paged_review = paginator.get_page(1)

    data = {
        'room': room,
        'reviews': paged_review,
    }
    return render(request, 'normal_user_room_read.html', {'reviews': paged_review})


def room_search(request):
    a = json.loads(requests.get('http://127.0.0.1:8000/db/room/').text)
    print(type(a))
    a=a+a+a+a+a+a
    print(a)
    return render(request, 'normal_user_room_search.html', {'rooms': a})
# 리뷰 열람 페이지
    # 해당 리뷰 정보를 받는다.
    # 해당 리뷰의 원룸의 주소를 바탕으로 관련 리뷰들을 받는다. (정렬 조건도 보내서)
    # 리뷰 정보와 리뷰 리스트를 context로 반환
    
    
# 관련 리뷰 반환
    # 입력 받은 원룸 주소를 기준으로 리뷰들을 구한다.
    # 구한 리뷰들을 반환한다.


# 원룸 열람 페이지
    # 해당 원룸 정보를 받는다.
    # 해당 원룸의 주소를 바탕으로 관련 리뷰들을 받는다. (정렬 조건도 보내서)
    # 원룸 정보와 리뷰 리스트를 context로 반환