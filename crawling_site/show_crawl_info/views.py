import datetime
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template

from show_crawl_info.models import Member, Question

from modules.baekjoon_crawling import Baekjoon

def get_time():
    now = datetime.datetime.now()
    formatted_time = f'{now.hour:02}:{now.minute:02}:{now.second:02}'
    return formatted_time

# db에 있는 최신 멤버랑 문제 정보 보여주기
def crawl_home(request):
    now = get_time()
    ##########임시로 사이트 들어가면 크롤링 바로 보여주기 
    # 나중에 db에서 데이터 불러오게 되면 지울 부분
    now = get_time()
    baek = Baekjoon()
    results = baek.get_all_results()
    ##################
    
    # 버튼을 누르면 최신 정보를 db에 저장하고 페이지 refresh하기
    if request.GET.get('print_btn'):
        now = get_time()
        baek = Baekjoon()
        results = baek.get_all_results()
        print(results)
        # update db -> result의 키 값은 (문제번호, 문제제목)
        # 여기 있는 if-else 다 create_of_get으로 없앨 수 있다?!
        for member_id, questions in results.items():
            # 멤버가 db에 있으면
            if Member.objects.filter(member_id=member_id).exists():
                m = Member.objects.get(member_id=member_id)
            # 멤버 db에 없으면 생성하고 저장
            else:
                m = Member(member_id=member_id)
                m.save()
                
            # update questions
            for question in questions:
                # 문제가 db에 있으면 그걸 멤버에 연결
                if Question.objects.filter(question_number=question[0]).exists():
                    q = Question.objects.get(question_number=question[0])
                # db에 해당 문제 추가 -> 첨 크롤링할 때 속성 더 가져와야됨 아예 결과도 dictionary 형태로 가져와보기
                else:
                    q = Question(question_number=question[0], question_title=question[1])
                    q.save()
                m.member_solved.add(q)
        print('최신 멤버 리스트: ', Member.objects.all())
        print('최신 문제 리스트: ', Question.objects.all())
        
        # refresh 는 자동으로 되게 됐네
    context = {'title': 'Welcome to Baekjoon Crawling Results', 'results': results, 'time': now}
    return render(request, 'crawl_home.html', context)

        