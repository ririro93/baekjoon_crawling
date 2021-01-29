from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template

from show_crawl_info.models import Member, Question

from modules.baekjoon_crawling import Baekjoon

def fines_home(request):
    # 일단 여기에 오늘의 현황 보여주자
    return render(request, 'fines_home.html')


    
    