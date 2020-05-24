from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from booktest.models import HeroInfo


def index(request):
    print(HeroInfo.objects.get(id=1))
    return HttpResponse('ok')
