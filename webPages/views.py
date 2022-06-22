from django.shortcuts import render
import requests
from django.http import HttpResponseRedirect


def main(request):
    # 쿠키에 토큰이 있다면 해당 토큰으로 로그인을 시도한다. == 토큰으로 값을 받아올 수 있는지 확인한다.
    # 이미 로그인 한 사이트에 대해, 창을 닫지 않는 한(탭만 닫았던 경우) 자동으로 로그인 되도록 하는 기능이다.
    if request.COOKIES.get('token'):
        token = request.COOKIES['token']
        # 토큰의 정보를 받는다.
        a = requests.get('https://kapi.kakao.com/v1/user/access_token_info', headers={'Authorization': 'Bearer '+token}).json()
        # 경고 메시지를 받은 경우 == 토큰이 유효하지 않은 경우이다.
        if a.get('msg'):
            return render(request, 'normal_user_base.html', {'alive': 'false'})
        # 토큰이 유효하다면 해당 토큰의 회원번호를 사용해, 회원의 retrieve 뷰를 이용하여 회원 정보를 구한다.
        else:
            user = requests.get('http://127.0.0.1:8000/db/user/'+str(a.get('id'))+'/').json()
            # 로그인 상태임을 나타내는 변수와 함께, 접속한 회원의 닉네임을 context로 함께 전달한다.
            return render(request, 'normal_user_base.html', {'alive': 'true', 'user': 'hi'})
    # 토큰이 쿠키에 없는 경우 == 로그인이 안 되는 경우
    else:
        # 그냥 메인 페이지로 이동한다.
        return render(request, 'normal_user_base.html', {'alive': 'false'})


# 로그인 시도 시에 처리되는 메소드
def login(request):
    # 쿠키의 토큰이 암호화되어 있지 않다고 가정
    token = request.COOKIES.get('token')
    code = dict(request.GET).get('code')
    print(token)

    # 토큰이 쿠키에 있지만 만료되었다면 토큰을 None으로 바꾼다.
    # 페이지마다 별도로 쿠키를 관리하기 때문에 우연히 토큰이 만료되었음에도 쿠키가 남는 경우가 생길 수 있다.
    if token != None:
        if requests.get('https://kapi.kakao.com/v1/user/access_token_info', headers={'Authorization': 'Bearer ' + token}).json().get('msg'):
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
            print(json_result)
            token = json_result['access_token']

    # 쿠키에 토큰이 있었거나, 새로 발급 받은 경우 여기로 와서 토큰으로 정보를 받는다.
    a = requests.get('https://kapi.kakao.com/v1/user/access_token_info', headers={'Authorization': 'Bearer ' + token}).json()
    # 토큰 정보 중 회원 정보를 이용하여 해당 회원이 가입되어 있는지 확인한다.
    user = requests.get('http://127.0.0.1:8000/db/user/' + str(a.get('id')) + '/').json()
    # 토큰에 해당하는 회원이 DB에 없다면 회원 가입 페이지로 이동한다.
    if user.get('detail') == 'Not found.':
        res = render(request, 'sign_up.html')
        res.set_cookie('token', token, max_age=18000)
        return res
    # 메인 페이지로 이동하는 render를 생성한다.
    res = render(request, 'normal_user_base.html', {'alive': 'true'})
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
    res = render(request, 'normal_user_base.html', {'alive': 'false'})
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
    requests.post('http://127.0.0.1:8000/db/user/', data=body)
    # 메인 페이지에 기본 상태로 이동하는 render를 작성한다.
    res = render(request, 'normal_user_base.html', {'alive': 'false'})
    # 만약 토큰이 쿠키에 존재한다면 쿠키에서 제거한다.
    res.delete_cookie('token')
    return res
