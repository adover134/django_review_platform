from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.core.paginator import Paginator
from customForms import reviewWriteForms


# 토큰의 유효 여부로 로그인 상태를 확인하는 함수이다.
# 토큰이 유효하다면 토큰의 정보들을 반환하고, 아니라면 None을 반환한다.
def tokencheck(token):
    a = requests.get('https://kapi.kakao.com/v1/user/access_token_info', headers={'Authorization': 'Bearer '+token}).json()
    # 경고 메시지를 받은 경우 == 토큰이 유효하지 않은 경우이다.
    if a.get('msg'):
        return None
    return a


#토큰 정보를 반환하는 함수이다.
#한 줄이지만 표현의 간소화를 위해 함수로 작성한다.
def tokeninfo(token):
    return requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": 'Bearer ' + token}).json()


#회원번호로 가입된 사람인지 확인한다. 가입되었다면 True를 반환한다.
def usercheck(u_id):
    user = requests.get('http://127.0.0.1:8000/db/user/' + u_id + '/').json()
    if user.get('detail') == 'Not found.':
        return None
    else:
        return user


# 경고횟수와 최근 경고일을 통해 접속 가능 여부를 확인한다. 접속 가능 시 True, 불가능 시 False를 반환한다.
def useralive(warn_count, penalty_date):
    # 경고 횟수가 20회라면 영구 탈퇴인 상태이다.
    if warn_count == 20:
        return 4

    # 만약 경고 횟수가 15회 이상이라면
    elif warn_count >= 15:
        # 최근 경고일을 확인한다.
        p_date = datetime.strptime(penalty_date, '%Y-%m-%d')
        # 경고일로부터 한 달 후의 날짜를 구한다.
        end_date = p_date + relativedelta(months=1)
        # 오늘 날짜를 구한다.
        today = datetime.today()
        # 한 달의 기간이 안 끝났다면 로그인이 안 된다.
        if today.year < end_date.year or (today.year == end_date.year and today.month < end_date.month) or (today.year == end_date.year and today.month == end_date.month and today.day < end_date.day):
            return 3
    # 로그인 가능 시 회원 정보 반환
    return True


@login_required(login_url='/login/')
def main(request):
    return render(request, 'normal_user_main.html')


# 로그인 시도 시에 처리되는 메소드
def login(request):
    return render(request, 'normal_user_main.html')


def logout(request):
    auth_logout(request)
    return redirect('/')


def signupPage(request):
    return render(request, 'normal_user_sign_up.html')


def signup(request):
    print(request.user)
    res = render(request, 'normal_user_main.html')
    return res


def infoCheck(request):
    token = request.COOKIES.get('token')
    if token:
        a = tokencheck(token)
        user = usercheck(str(a.get('id')))
        print(user)
        userForm = reviewWriteForms.UserInfoForm(initial={'user_nickname': user.get('uNickname'), 'user_email': user.get('uEmail'), 'user_warn_count': user.get('uWarnCount')})
        if not user:
            return render(request, 'normal_user_info_check.html', {'alive': 'false'})
        else:
            return render(request, 'normal_user_info_check.html', {'alive': 'true', 'user': user, 'userForm': userForm})
    else:
        return render(request, 'normal_user_info_check.html', {'alive': 'false'})


def normal_user_review_search(request):
    review_search_url = 'http://127.0.0.1:8000/db/review/'
    print(request.user)
    data = dict(request.GET)
    review_search_url = review_search_url+'?'
    print(data)
    if data.get('builtFrom') and data.get('builtTo'):
        review_search_url = review_search_url+'builtFrom='+data.get('builtFrom')[0]+'&builtTo='+data.get('builtTo')[0]
    if data.get('address'):
        if review_search_url[-1] != '?':
            review_search_url = review_search_url+'&'
        review_search_url = review_search_url+'address='+data.get('address')[0]
    for i in range(3):
        if data.get('commonInfo'):
            for c in data.get('commonInfo'):
                review_search_url = review_search_url+'&'+'commonInfo='+c
    review_list = json.loads(requests.get(review_search_url).text)
    paginator = Paginator(review_list, 5)
    page = request.GET.get('page')
    paged_review = paginator.get_page(page)
    token = request.COOKIES.get('token')
    context = {'paged_review': paged_review}
    if token:
        a = tokencheck(token)
        context['alive'] = 'true'
        user = usercheck(str(a.get('id')))
        context['user'] = user.get('uNickname')
    return render(request, 'normal_user_review_search.html', context)


def normal_user_review_read(request):
    token = request.COOKIES.get('token')
    user = None
    if token:
        a = tokencheck(token)
        user = usercheck(str(a.get('id')))
    review = None
    review_num = request.GET.get('id')
    print(review_num)
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
    if user:
        # 해당 리뷰에 대해 추천한 사람 중 사용자가 있는지 확인
        recommended = None
        reported = None
        recommends = review.get('recommendedOn')
        print('w')
        if recommends:
            for recommend in recommends:
                print(recommend)
                if json.loads(requests.get(recommend).text).get('uId') == user.get('uId'):
                    recommended = True
                    break
        # 해당 리뷰에 대해 신고한 사람 중 사용자가 있는지 확인
        reports = review.get('reportedOn')
        if reports:
            for report in reports:
                if json.loads(requests.get(report).text).get('uId') == user.get('uId'):
                    reported = True
                    break
        return render(request, 'normal_user_review_read.html', {'review': review, 'icons': icons, 'alive': 'true', 'user': user.get('uNickname'), 'userInfo': user, 'recommended': recommended, 'reported': reported})
    else:
        return render(request, 'normal_user_review_read.html', {'review': review, 'icons': icons, 'alive': 'false'})


@api_view(['POST'])
def normal_user_review_recommend(request):
    data = dict(request.POST)
    token = request.COOKIES.get('token')
    user = None
    if token:
        a = tokencheck(token)
        user = usercheck(str(a.get('id')))
    if user:
        # 로그인이 되어 있다면 해당하는 리뷰 번호와 사용자 번호로 추천 내역을 DB에 추가한다.
        if data.get('recommended')[0] == 'false':
            data1 = {'uId': user.get('uId'), 'reviewId': int(data.get('review')[0])}
            print(data1)
            a = requests.post('http://127.0.0.1:8000/db/recommend/', data=data1)
        else:
            # 리뷰 번호와 사용자 번호로 추천 내역을 찾아서 삭제한다.
            url = 'http://127.0.0.1:8000/db/recommend/?reviewId='+str(data.get('review')[0])+'&uId='+str(user.get('uId'))
            a = requests.get(url)
            requests.delete('http://127.0.0.1:8000/db/recommend/'+a.text)
    return Response('success')


@api_view(['POST'])
def normal_user_review_report(request):
    data = dict(request.POST)
    token = request.COOKIES.get('token')
    user = None
    if token:
        a = tokencheck(token)
        user = usercheck(str(a.get('id')))
    if user:
        # 로그인이 되어 있다면 해당하는 리뷰 번호와 사용자 번호로 추천 내역을 DB에 추가한다.
        if data.get('reported')[0] == 'false':
            data1 = {'uId': user.get('uId'), 'reviewId': int(data.get('review')[0])}
            print(data1)
            a = requests.post('http://127.0.0.1:8000/db/report/', data=data1)
        else:
            # 리뷰 번호와 사용자 번호로 추천 내역을 찾아서 삭제한다.
            url = 'http://127.0.0.1:8000/db/report/?reviewId='+str(data.get('review')[0])+'&uId='+str(user.get('uId'))
            a = requests.get(url)
            print(a.text)
            requests.delete('http://127.0.0.1:8000/db/report/'+a.text+'/?user=1')
    return Response('success')
