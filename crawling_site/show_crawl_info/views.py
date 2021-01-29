from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template

from show_crawl_info.models import Question, Choice

from modules.baekjoon_crawling import Baekjoon

def crawl_home(request):
    # 일단 여기에 오늘의 현황 보여주자
    baek = Baekjoon()
    results = baek.get_all_results()
    context = {'title': 'Welcome to Baekjoon Crawling Results', 'results': results}
    return render(request, 'crawl_home.html', context)


    