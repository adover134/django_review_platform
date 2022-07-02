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
    if request.method == 'POST':
        form = forms.TextReviewWriteForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')
        print(images)
        if form.is_valid():
            names = handle_uploaded_file(images)
        print(form)
    else:
        form = forms.TextReviewWriteForm()
    return render(request, 'normal_user_review_write.html', {'form': form})


def handle_uploaded_file(f):
    names = []
    for image in f:
        print(image)
        with open('static/images/'+image.name, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        names.append(image.name)
    return names

def normal_user_review_write_page(request):
    return render(request, 'normal_user_review_write.html', {'form':forms.ReviewForm})


def image(request):
    print(request.GET)
    return render(request, 'normal_user_review_search.html')
