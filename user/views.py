#!/usr/bin/python3
from django.shortcuts import render
from django.http import HttpResponse
from dao.GifImage import GifImageHelper
import json
import pymysql
import datetime
import pymysql.cursors
import logging
import random

pymysql.install_as_MySQLdb()

def index(request):
    return render(request, 'home.html')

def getGifs(request):
    if request.method == 'GET':
        page = int(request.GET.get('page', 0))
        helper = GifImageHelper()
        gifs = helper.getGifs(page)
        return HttpResponse(json.dumps(gifs, sort_keys=True))

def bindphone(request):
    # 绑定phone 和 wxuuid
    logging.info('start bindphone request')
    if request.method == 'POST':
        phone = request.POST['phone']
        wxuuid = request.POST['wxuuid']

        connection = pymysql.connect(host='104.128.91.88',
                        port=3306,
                        user='root',
                        passwd='911220',
                        db='wolfman',
                        charset='utf8',
                        cursorclass=pymysql.cursors.DictCursor)

        helper = DBHelper()
        isb = helper.checkIsBind(wxuuid)
        if isb != True:
            print('已经绑定phone')
            data = {'code':0,'data':{},'msg': 'no nessesary to bind'}
            return HttpResponse(json.dumps(data, sort_keys=True))
        else:
            helper.bindPhone(phone, wxuuid)
            data = {'code':0,'data':{},'msg': 'bind success'}
            data2 = {'phone':phone}
            data['data'] = data2
            return HttpResponse(json.dumps(data, sort_keys=True))
    else:
        return '123'

def getPic(request):
    print('get pics')
    if request.method == 'POST':
        page = request.POST['page']
        print('page:' + str(page))
        helper = DBHelper()
        data = helper.getPics(page)
        return HttpResponse(json.dumps(data, sort_keys=True))
    else:
        return HttpResponse("")

def getPornPics(request):
    if request.method == 'POST':
        page = request.POST['page']
        helper = DBHelper()
        data = helper.getPornPics(page)
        return HttpResponse(json.dumps(data, sort_keys=True))

def getPornTitles(request):
    print('getPornTitles')
    if request.method == 'POST':
        page = request.POST['page']
        helper = DBHelper()
        data = helper.getPornTitles(page)
        return HttpResponse(json.dumps(data, sort_keys=True))

def getPicsByTitle(request):
    print('getPicsByTitle')
    if request.method == 'POST':
        title = request.POST['title']
        helper = DBHelper()
        data = helper.getPicsByTitle(title)
        return HttpResponse(json.dumps(data, sort_keys=True))

def test_python(request):
    # 改接口用于测试python语法
    print('start test_python request')
    helper = DBHelper()
    data = helper.test()
    return HttpResponse(data)

    if request.method == 'GET':
        phone = request.GET['phone']
        wxuuid = request.GET['wxuuid']

        helper = DBHelper()

        isb = helper.checkIsBind(wxuuid)
        if isb != True:
            return HttpResponse('already binded')
        else:
            helper.bindPhone(phone, wxuuid)
            data = {'code':0,'data':{},'msg': 'bind success'}
            data2 = {'phone':phone}
            data['data'] = data2
            return HttpResponse(json.dumps(data, sort_keys=True))
        print(s)

    return HttpResponse(s)

class DBHelper:

    def __init__(self):
        self.config = {
            'host' : '104.128.91.88',
            'port' : 3306,
            'user' : 'root',
            'passwd' : '911220',
            'db' : 'porn',
            'charset' : 'utf8',
            'cursorclass' : pymysql.cursors.DictCursor
        }

    # 链接数据库，回头设计个连接池
    def connectDB(self):
        self.connection = pymysql.connect(**self.config)

    # 关闭数据库
    def closeDB(self):
        self.connection.close()

    # 检测是否需要绑定
    def checkIsBind(self, wxuuid):
        # sql
        self.connectDB()
        sql = " select * from User where User.id = '%s' " % (wxuuid)
        cur = self.connection.cursor()
        result = cur.execute(sql)
        data = cur.fetchone()

        self.closeDB()

        print("data:  " + json.dumps(data, sort_keys=True))
        if data != None and len(data) != 0:
            if data.get('phone'):
                print(data.get('phone'))
                return False
            else:
                return True
        else:
            return False

    def bindPhone(self, phone, wxuuid):
        self.connectDB()
        sql_pattern = "update User set User.phone = '%s' where User.id = '%s' " % (phone, wxuuid)
        print(sql_pattern)
        cur = self.connection.cursor()
        cur.execute(sql_pattern)
        # 提交后生效
        self.connection.commit()
        self.closeDB()

    def getPics(self, page):
        self.connectDB()
        sql = "select url from douban_pic order by url asc limit %s,10"
        # sql = "select url from douban"
        print(sql)
        cur = self.connection.cursor()
        cur.execute(sql, (int(page) * 10,))
        data = cur.fetchall()
        print(data)
        self.closeDB()
        return data

    def getPornPics(self, page):
        self.connectDB()
        cur = self.connection.cursor()
        sql = "select * from bbs_91porn limit %s,15"
        cur.execute(sql, (int(page) * 10,))
        data = cur.fetchall()
        print(data)
        self.closeDB()
        return data

    def getPornTitles(self, page):
        self.connectDB()
        cur = self.connection.cursor()
        sql = "select count(*) as sum, title, url, new_url from bbs_91porn group by title limit %s,15"
        cur.execute(sql, (int(page) * 10,))
        data = cur.fetchall()
        print(data)
        self.closeDB()
        return data

    def getPicsByTitle(self, title):
        self.connectDB()
        cur = self.connection.cursor()
        sql = "select title, url, new_url from bbs_91porn where title=%s"
        cur.execute(sql, (title,))
        data = cur.fetchall()
        print(data)
        self.closeDB()
        return data

    def test(self):
        # self.connectDB()
        self.connectDB()
        # namelist = []
        file_object = open('./user/a')
        cur = self.connection.cursor()
        try:
            for line in file_object:
                # 忽略换行符
                line=line.strip('\n')
                if line:
                    sql_pattern = "insert into User(id, nickname, sex, liveness, phone, state) values ('%s','%s','%s','%s','%s','%s'); " % (str(random.randint(100000, 999999)), line, str(random.randint(0, 2)), str(random.randint(0, 1000)),
                    "1876817" + str(random.randint(1000, 9999)), str(random.randint(0, 2)))
                    print(sql_pattern)
                    cur.execute(sql_pattern)
                # namelist.append(line)
        finally:
            file_object.close()
        # return json.dumps(namelist, sort_keys=True, ensure_ascii=False)
        self.connection.commit()
        self.closeDB()
        return ""
