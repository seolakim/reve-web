from django.shortcuts import render, render_to_response
from django.utils import timezone
from django.http import HttpResponse, Http404
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.paginator import EmptyPage, PageNotAnInteger
from flynsarmy_paginator.paginator import FlynsarmyPaginator as Paginator
from .models import gn
from django.db.models import Q
import random
import pymysql

ITEMS_PER_PAGE = 10
PAGE_GROUP = 10

#-- TemplateView
def home(request):
    return render(request, 'foodle/home.html')

def search(request):
    wisesaying = [
        '고기 먹다 체하면 냉면으로 쑥 눌러줘라',
        '기분이 저기압일 땐 반드시 고기 앞으로 가라',
        '내가 아는 맛이 가장 맛있는 맛',
        '치킨 뼈를 봤을 때 앙념을 먹었는지 후라이드를 먹었는지 모르게 하라',
        '맛있게 먹으면 0칼로리',
        '탕수육은 부먹도 찍먹도 아닌 쳐먹이 진리',
        '일찍 일어나는 새가 많이 먹는다',
        '먹었던 뼈도 다시보자',
        '인생은 치킨의 연속이다',
        '내가 먹겠다는 의지만 있으면 위가 늘어난다',
        'B(birth)와 D(death)사이에는 C(chicken)이 있다',
        '오늘 먹을 치킨을 내일로 미루지 말자',
        '튀긴 음식은 신발을 튀겨도 맛있다',
        '맛집이 있다면 지옥도 가겠다',
        '현기증 난단 말이에요. 빨리 라면 끓여 주세요',
        '물이 너무 많으면 라면을 더 넣어라',
    ]



    if not hasattr(search, "searchwords"):
        search.searchwords = ''
    if not hasattr(search, "foodle_list"):
        search.foodle_list = []
    if not hasattr(search, "w_list"):
        search.w_list = []


    if 'search_words' in request.GET:
        search.searchwords = request.GET['search_words']

        if search.searchwords == '':
            search.foodle_list = []
        else:
            #search.foodle_list = mysqlexport(search.searchwords)
            search.w_list = wordslist(search.searchwords)
            q =Q(title__contains=search.searchwords) | Q(subtitle__contains=search.searchwords) | Q(ind__contains=search.searchwords)
            for wlist in search.w_list:
                q = q | (Q(title__contains=wlist) | Q(subtitle__contains=wlist) | Q(ind__contains=wlist))
            search.foodle_list = gn.objects.filter(q).order_by('-data')

    # Paging
    paginator = Paginator(search.foodle_list, 10, adjacent_pages = 5)

    page = request.GET.get('page')
    try:
        lists = paginator.page(page)
    except PageNotAnInteger:
        lists = paginator.page(1)
    except EmptyPage:
        lists = paginator.page(paginator.num_pages)

    return render_to_response('foodle/search.html', {"lists": lists, "searchwords": search.searchwords, "wisesaying": wisesaying[random.randint(0, len(wisesaying)-1)]})

#search_list.searchwords=''


def mysqlexport(key):
    conn=pymysql.connect(host='127.0.0.1',charset='utf8',user='root',passwd='root',db='food')
    conn.query("set character_set_connection=utf8;")
    conn.query("set character_set_server=utf8;")
    conn.query("set character_set_client=utf8;")
    conn.query("set character_set_results=utf8;")
    conn.query("set character_set_database=utf8;")
    curs = conn.cursor(pymysql.cursors.DictCursor)
    key = searchword(key)
    sql="SELECT * FROM gn where title like" + key + " or ind like " + key + " or subtitle like " + key + "ORDER BY data DESC"
    print(sql)
    curs.execute(sql)
    rows=curs.fetchall()
    return rows

def searchword(key):
    sc=0
    ec=0
    cc=0
    wnum=0
    word=''
    for a in key:
        cc+=1

        if a.count(' ')>0:
            ec=cc-1
            word+=" '%"+key[sc:ec]+"%' and ind like"
            sc = cc
        if cc==key.__len__():
            ec=cc
            word += " '%" + key[sc:ec] + "%'"
            sc ==cc
    return word

def wordslist(key):
    words_list = []
    temp = ''
    cc = 0

    for a in key:
        cc += 1
        if a==' ':
            words_list.append(temp)
            temp = ''
        else:
            temp += a
            if(cc == len(key)):
                words_list.append(temp)

    return words_list

#mysqlexport('서울   프뤼엥   ')
