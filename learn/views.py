#coding:utf-8
from django.http import HttpResponse

def index(request):
    response = u'''{
        a : 1,
        b : 3
    }'''
    return HttpResponse(response)
