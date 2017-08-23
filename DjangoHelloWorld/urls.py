#coding:utf-8
from django.conf.urls import include, url
from django.contrib import admin
from learn import views as learn_views
from user import views as user_views

urlpatterns = [
    url(r'^$', learn_views.index),
    url(r'^$', user_views.index, name='home'),
    url(r'^admin/', include(admin.site.urls)),

    # 用户部分接口
    url(r'^bindphone$', user_views.bindphone, name='bindphone'),
    url(r'^getPic$', user_views.getPic, name='getPic'),
    url(r'^getPornPics$', user_views.getPornPics, name='getPornPics'),
    url(r'^getPornTitles$', user_views.getPornTitles, name='getPornTitles'),
    url(r'^getPicsByTitle$', user_views.getPicsByTitle, name='getPicsByTitle'),

    # 测试语法接口
    url(r'^test_python$', user_views.test_python, name='test'),


    # Gif 图片接口
    url(r'^getGifs$', user_views.getGifs, name='getGifs'),
]
