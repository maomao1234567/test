# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from . import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math

from django.http import HttpResponse
from django.template import loader
from pyecharts import Line3D
REMOTE_HOST = "https://pyecharts.github.io/assets/js"
from pyecharts import WordCloud
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def index(request):
    books = models.Book6.objects.all()
    paginator = Paginator(books, 10)
    page = request.GET.get('page')
    try:
        book = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        book = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        book = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'book': book})


def book_page(request, serial_name):
    book = models.Book6.objects.get(pk=serial_name)
    return render(request, 'book_page.html', {'book': book})


def search_page(request):

    p = request.GET.get('p')
    error_msg=''

    if not p:
        error_msg ='please input right words'
        return render(request,'error.html',{'error_msg':error_msg})

    post_list =models.Book6.objects.filter(serial_name__icontains=p) #相当于数据库的模糊查询
    return render(request, 'error.html',{'error_msg': error_msg,'post_list': post_list})

def hh(request):
    template = loader.get_template('web6/pyecharts.html')
    l3d = wordcloud()
    context = dict(
        myechart=l3d.render_embed(),
        host=REMOTE_HOST,
        script_list=l3d.get_js_dependencies()
    )
    return HttpResponse(template.render(context, request))


"""
def line3d():
    _data = []
    for t in range(0, 25000):
        _t = t / 1000
        x = (1 + 0.25 * math.cos(75 * _t)) * math.cos(_t)
        y = (1 + 0.25 * math.cos(75 * _t)) * math.sin(_t)
        z = _t + 2.0 * math.sin(75 * _t)
        _data.append([x, y, z])
    range_color = [
        '#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
        '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
    line3d = Line3D("3D line plot demo", width=1200, height=600)
    line3d.add("", _data, is_visualmap=True,
               visual_range_color=range_color, visual_range=[0, 30],
               is_grid3D_rotate=True, grid3D_rotate_speed=180)
    return line3d
"""

def wordcloud():
    """with open('myweb6/book6.txt', 'r') as f:
        comment =f.read()
        comment_list = comment.split('\n')

        data = []
        for commet in comment_list:
            commet1 = commet
            data.append(commet1)
        c = range(500, 745)
        value = random.sample(c, 245)"""
    name = [
            '带一本书去巴黎','变形记','阿狸·梦之城堡','平凡的世界（全三部）','苏菲的世界','送你一颗子弹','天才在左 疯子在右','嫌疑人X的献身','人生','陆犯焉识','雷雨',
'你今天真好看','爱的艺术','撒哈拉的故事','笑傲江湖（全四册）','第一炉香','不能承受的生命之轻','飘','天龙八部','三体Ⅱ',]
    value1 = [
            10000, 6181, 4386, 4055, 2467, 2244, 1898, 1484, 1112,
            965, 847, 582, 555, 550, 462, 366, 360, 282, 273, 265]
    wordcloud = WordCloud(width=400, height=600)
    wordcloud.add('', name, value1, word_size_range=None)
    return wordcloud







