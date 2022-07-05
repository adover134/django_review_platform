from django.shortcuts import render
from django.core.paginator import Paginator
from DBs.models import Review, User
from webPages import views
import requests
import json
from forms import forms


def base(request):
    return render(request, 'base.html')


def normal_user_base(request):
    return render(request, 'normal_user_base.html')


def normal_user_review_search(request):
    review_search_url = 'http://127.0.0.1:8000/db/review/'
    if request.POST:
        #print(int(request.POST.get('built_from')))
        print(request.POST)
        data = dict(request.POST)
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


def normal_user_review_write(request):
    form = None
    user = None
    review_id = None
    token = request.COOKIES.get('token')
    if token:
        a = views.tokencheck(token)
        user = views.usercheck(str(a.get('id')))
    if request.method == 'POST':
        data = dict(request.POST)
        data1 = {}
        if data.get('review_type')[0] == 'text':
            form = forms.TextReviewWriteForm(request.POST, request.FILES)
            data1['reviewKind'] = 0
            data1['reviewSentence'] = data['review_sentence']
        else:
            form = forms.ImageReviewWriteForm(request.POST, request.FILES)
            data1['reviewKind'] = 1
        images = request.FILES.getlist('images')
        if form.is_valid():
            data1['reviewTitle'] = data['title']
            # 주소로 원룸을 검색한다.
            room = json.loads(requests.get('http://127.0.0.1:8000/db/room/?address='+data['address'][0]).text)
            # 만약 없다면, 임의로 주소만 있는 원룸 객체를 만들어서 저장한다.
            '''
            
            '''
            # 원룸 번호를 구한다.
            data1['roomId'] = room[0].get('id')
            data1['uId'] = user.get('uId')
            review = requests.post('http://127.0.0.1:8000/db/review/', data=data1)
            review_id = json.loads(review.text).get('id')
            names = handle_uploaded_file(images)
            for name in names:
                requests.post('http://127.0.0.1:8000/db/image/', data={})
    return render(request, 'normal_user_review_read.html', {'review_num': review_id})


def handle_uploaded_file(f):
    names = []
    for image in f:
        with open('static/images/'+image.name, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        names.append('static/images/'+image.name)
    return names


def normal_user_review_write_page(request):
    form = {'TextForm': forms.TextReviewWriteForm, 'ImageForm': forms.ImageReviewWriteForm}
    token = request.COOKIES.get('token')
    if token:
        a = views.tokencheck(token)
        user = views.usercheck(str(a.get('id')))
        if user:
            form['alive'] = 'true'
        else:
            form['alive'] = 'false'
    return render(request, 'normal_user_review_write.html', form)


def normal_user_review_read(request):
    token = request.COOKIES.get('token')
    user = None
    if token:
        a = views.tokencheck(token)
        user = views.usercheck(str(a.get('id')))
    review = None
    review_num = request.GET.get('id')
    print(review_num)
    review = json.loads(requests.get('http://127.0.0.1:8000/db/review/'+review_num+'/').text)
    address = json.loads(requests.get('http://127.0.0.1:8000/db/room/'+str(review.get('roomId'))+'/').text).get('address')
    review['address'] = address
    if user:
        return render(request, 'normal_user_review_read.html', {'review': review, 'alive': 'true'})
    else:
        return render(request, 'normal_user_review_read.html', {'review': review, 'alive': 'false'})


def image(request):
    print(request.GET)
    return render(request, 'normal_user_review_search.html')
