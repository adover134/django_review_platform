from django.shortcuts import render
import requests
import json
from django.http import HttpResponseRedirect
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


def main(request):
    # 쿠키에 토큰이 있다면 해당 토큰으로 로그인을 시도한다. == 토큰으로 값을 받아올 수 있는지 확인한다.
    # 이미 로그인 한 사이트에 대해, 창을 닫지 않는 한(탭만 닫았던 경우) 자동으로 로그인 되도록 하는 기능이다.
    token = request.COOKIES.get('token')
    if token:
        # 토큰 주인의 회원번호를 받는다.
        a = tokencheck(token)
        # 회원 번호를 받지 못했다면
        if not a:
            return render(request, 'normal_user_main.html', {'alive': 'false'})
        # 토큰이 유효하다면 해당 토큰의 회원번호를 사용해, 회원의 retrieve 뷰를 이용하여 회원 정보를 구한다.
        else:
            user = usercheck(str(a.get('id')))
            if not user:
                return render(request, 'normal_user_main.html', {'alive': 'false'})
            else:
                # 로그인 상태임을 나타내는 변수와 함께, 접속한 회원의 닉네임을 context로 함께 전달한다.
                return render(request, 'normal_user_main.html', {'alive': 'true', 'user': user['uNickname']})
    # 토큰이 쿠키에 없는 경우 == 로그인이 안 되는 경우
    else:
        # 그냥 메인 페이지로 이동한다.
        return render(request, 'normal_user_main.html', {'alive': 'false'})


# 로그인 시도 시에 처리되는 메소드
def login(request):
    # 쿠키의 토큰이 암호화되어 있지 않다고 가정
    token = request.COOKIES.get('token')
    code = dict(request.GET).get('code')

    '''
    카카오에 로그인이 되어 있다면
    1. 토큰이 살아 있는 경우
    2. 토큰을 받기 위한 인가코드를 받은 경우
    위의 2가지이다.
    
    토큰이 있다면 살아있는지 체크해서, 살아있지 않다면 로그인 창으로 보낸 후 돌아오도록 한다.
    토큰이 없다면 코드를 받아서 토큰을 받는다.
    
    이렇게 해서 살아있는 토큰을 얻어야 한다.
    '''

    # 토큰이 쿠키에 있지만 만료되었다면 토큰을 None으로 바꾼다.
    if token:
        if not tokencheck(token):
            token = None
    # 쿠키에 토큰이 없다면 새로 만들도록 한다.
    if token is None:
        # 로그인 창을 거치지 않았다면 로그인 창으로 이동시킨다. 만약 카카오 로그인이 되어있다면 바로 이 메소드로 돌아온다.
        if code == None:
            return HttpResponseRedirect('https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=dc1611725046556aa00ee3cd0fcc253f&redirect_uri=http://127.0.0.1:8000/login&response_type=code')
        # 로그인 창을 거쳤다면 인가코드를 갖고 있다.
        else:
            # 인가코드로 토큰을 받기 위해 변수들을 설정한다.
            # 권한 타입은 코드를 이용하는 방식으로 지정한다.
            grant_type = 'authorization_code'
            # 클라이언트 아이디는 REST api 키를 이용한다.
            client_id = 'dc1611725046556aa00ee3cd0fcc253f'
            # 이 메소드를 실행시키기 위한 URI를 준다.
            redirect_uri = 'http://127.0.0.1:8000/login'
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

    '''
    살아있는 토큰이 있다면 토큰의 회원번호를 얻을 수 있다.
    DB에서 회원번호로 검색해서 가입된 사람인지 확인한다.
    가입되었다면 로그인이 가능한지 확인한다.
    아니라면 회원가입 페이지로 보낸다.
    '''

    # 쿠키에 토큰이 있었거나, 새로 발급 받은 경우 여기로 와서 토큰으로 회원번호를 얻는다.
    a = tokencheck(token)
    # 토큰 정보 중 회원 정보를 이용하여 해당 회원이 가입되어 있는지 확인한다.
    user = usercheck(str(a.get('id')))
    # 토큰에 해당하는 회원이 DB에 없다면 회원 가입 페이지로 이동한다.
    if not user:
        res = render(request, 'normal_user_sign_up.html')
        res.set_cookie('token', token, max_age=18000)
        return res
    # 만약 회원이 접속이 가능한 상태라면 메인 페이지로 이동하는 render를 생성한다.
    userstate = useralive(user.get('uWarnCount'), user.get('penaltyDate'))
    if userstate < 3:
        res = render(request, 'normal_user_main.html')
        # 토큰을 쿠키로 추가한다. 쿠키는 5시간만 지속되도록 한다.
        res.set_cookie('token', token, max_age=18000)
    elif userstate == 3:
        res = render(request, 'normal_user_main.html', {'msg': '경고 누적으로 로그인이 제한된 회원입니다.'})
    else:
        res = render(request, 'normal_user_main.html', {'msg': '경고 누적으로 로그인이 불가능한 회원입니다.'})
    return res


def logout(request):
    # 토큰의 생존 여부를 false로 하여 메인페이지로 이동시킬 준비를 한다.
    res = render(request, 'normal_user_main.html', {'alive': 'false'})
    # 현재 토큰을 쿠키에서 구한다.
    if request.COOKIES.get('token'):
        token = request.COOKIES.get('token')
        # 토큰이 살아있다면 만료시킨다.
        if tokencheck(token):
            requests.post('https://kapi.kakao.com/v1/user/logout', headers={"Authorization": 'Bearer '+token})
        # 쿠키에서 토큰을 제거한다.
        res.delete_cookie('token')
    return res


def signupPage(request):
    return render(request, 'normal_user_sign_up.html')


def signup(request):
    token = request.COOKIES.get('token')
    # 토큰 정보로 사용자 정보를 얻는다.
    a = tokeninfo(token)
    print(a)
    # 획득한 사용자 정보를 바탕으로 DB에 넣을 값들을 정한다.
    body = {
        'uId': a.get('id'),
        'uNickname': a.get('properties').get('nickname'),
        'uEmail': a.get('kakao_account').get('email'),
        'uAccessToken': token
    }
    # 새로운 회원을 DB에 추가하는 뷰를 수행한다.
    requests.post('http://127.0.0.1:8000/db/user/', data=body)
    # 메인 페이지에 기본 상태로 이동하는 render를 작성한다.
    res = render(request, 'normal_user_main.html', {'alive': 'false'})
    # 만약 토큰이 쿠키에 존재한다면 쿠키에서 제거한다.
    res.delete_cookie('token')
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
    print(data)
    review_search_url = review_search_url+'?'
    print(data)
    if data.get('builtFrom') and data.get('builtTo'):
        review_search_url = review_search_url+'builtFrom='+data.get('builtFrom')[0]+'&builtTo='+data.get('builtTo')[0]
    if data.get('address') != '':
        if review_search_url[-1] != '?':
            review_search_url = review_search_url+'&'
        #review_search_url = review_search_url+'address='+data.get('address')
    for i in range(3):
        if data.get('commonInfo_'+str(i+1)):
            review_search_url = review_search_url+'&'+'commonInfo_'+str(i+1)+'=on'
    review_list = json.loads(requests.get(review_search_url).text)
    print(review_list)
    paginator = Paginator(review_list, 3)
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
