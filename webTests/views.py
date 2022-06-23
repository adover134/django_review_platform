from django.shortcuts import render


def base(request):
    return render(request, 'base.html')


def normal_user_base(request):
    return render(request, 'normal_user_base.html')
