from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template

from show_crawl_info.models import Question, Choice

from modules.baekjoon_crawling import Baekjoon

def home_page(request):
    # show home page of the whole website
    return render(request, 'home_page.html')


    