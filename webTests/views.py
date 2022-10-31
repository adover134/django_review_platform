from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.decorators import api_view
from webPages import views
import requests
import json
from customForms import customForms


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def base(request):
    return render(request, 'base.html')


def normal_user_base(request):
    return render(request, 'normal_user_base.html')


def normal_user_review_search(request):
    review_search_url = 'http://127.0.0.1:8000/db/review/'
    data = dict(request.GET)
    print(data)
    review_search_url = review_search_url+'?'
    if data.get('builtFrom') and data.get('builtTo'):
        review_search_url = review_search_url+'builtFrom='+data.get('builtFrom')[0]+'&builtTo='+data.get('builtTo')[0]
    if data.get('address')[0] != '':
        if review_search_url[-1] != '?':
            review_search_url = review_search_url+'&'
        review_search_url = review_search_url+'address='+data.get('address')[0]
    for i in range(3):
        if data.get('commonInfo_'+str(i+1)):
            review_search_url = review_search_url+'&'+'commonInfo_'+str(i+1)+'=on'
    print(review_search_url)
    review_list = json.loads(requests.get(review_search_url).text)
    print(review_list)
    paginator = Paginator(review_list, 3)
    page = request.GET.get('page')
    paged_review = paginator.get_page(page)
    token = request.COOKIES.get('token')
    context = {'paged_review': paged_review}
    if token:
        if views.tokencheck(token):
            context['alive'] = 'true'
    return render(request, 'normal_user_review_search.html', context)


@api_view(['POST'])
def normal_user_review_write(request):
    user = request.user
    review_id = None
    if request.method == 'POST':
        data = dict(request.POST)
        data1 = {}
        form = customForms.TextReviewWriteForm(request.POST, request.FILES)
        data1['reviewSentence'] = data['review_sentence']
        images = request.FILES.getlist('images')
        print(form)
        if form.is_valid():
            print(request.POST)
            print(request.FILES)
            data1['reviewTitle'] = data['title']
            # 주소로 원룸을 검색한다.
            room = json.loads(requests.get('http://127.0.0.1:8000/db/room/?address='+data['address'][0]).text)
            # 만약 없다면, 임의로 주소만 있는 원룸 객체를 만들어서 저장한다.
            '''
            
            '''
            # 원룸 번호를 구한다.
            print(room)
            data1['roomId'] = room[0].get('id')
            data1['uId'] = user.id
            review = requests.post('http://127.0.0.1:8000/db/review/', data=data1)
            review_id = json.loads(review.text).get('id')
            for image in images:
                img = json.loads(requests.post('http://127.0.0.1:8000/db/reviewImage/', data={'reviewId': review_id}).text)
                img_name = handle_uploaded_file(image, str(img.get('id')))
                requests.put('http://127.0.0.1:8000/db/reviewImage/'+str(img.get('id'))+'/', data={'reviewId': review_id, 'image': img_name})
        return Response(str(review_id))


def handle_uploaded_file(f, name):
    with open('static/images/'+name+'.png', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return name+'.png'


def image(request):
    return render(request, 'normal_user_review_search.html')


def review_search_page(request):
    return render(request, 'tt.html')


def review_search_test(request):
    return render(request, 'index.html', {})
