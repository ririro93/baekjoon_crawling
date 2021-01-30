import datetime
import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.serializers.json import DjangoJSONEncoder
from django.template.loader import get_template
from rest_framework import viewsets
from rest_framework import permissions

 
from show_crawl_info.models import Question, Member, Solve
from show_crawl_info.serializers import MemberSerializer, SolveSerializer

from modules.baekjoon_crawling import Baekjoon

def get_time():
    now = datetime.datetime.now()
    formatted_time = f'{now.hour:02}:{now.minute:02}:{now.second:02}'
    return formatted_time

# db에 있는 최신 멤버랑 문제 정보 간략하게 보여주기
def crawl_home(request):

    ## init
    keys_for_Question = (
        'question_number',
        'question_site',
        'question_tier',
        'question_title',
    )
    update_time = get_time()
    
    ## 버튼을 누르면 최신 정보를 db에 저장하기
    if request.GET.get('print_btn'):
        update_time = get_time()
        baek = Baekjoon()
        results = baek.get_all_results()
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
                
            # update questions (solved time정보는 빼고 넣기)
            # questions가 최신께 앞에 들어있어서 전에 푼 시간이 최근에 푼 시간을 덮어씌움
            # -> 역행하도록 설정
            for question in questions[::-1]:
                # 문제가 db에 있으면 그걸 멤버에 연결
                if Question.objects.filter(question_number=question['question_number']).exists():
                    q = Question.objects.get(question_number=question['question_number'])
                # db에 해당 문제 추가 -> 첨 크롤링할 때 속성 더 가져와야됨 아예 결과도 dictionary 형태로 가져와보기
                else:
                    q = Question(**{key: question[key] for key in keys_for_Question})
                    q.save()
                # get date info and add to Solve
                solved_time = question['solved_time']
                formatted_solved_time = map(int, [solved_time[:4], solved_time[5:7], solved_time[8:10], solved_time[-8:-6], solved_time[-5:-3]])
                
                # 이 사람이 과거에 이 문제 푼적있으면 업데이트 없으면 생성
                solve, created_bool = Solve.objects.update_or_create(
                    question=q,
                    member=m,
                    defaults={'solved_time': datetime.datetime(*formatted_solved_time)},
                )
                solve.save()
                
    ## url 들어가면 실행될 부분
    # 일단 오늘 푼 문제 데이터 몽땅 다 넘겨보기
    results = {}
    members = Member.objects.all()
    for member in members:
        datas = member.get_member_solves_today()
        result = [{
            'q_num':data.question.question_number,
            'q_title':data.question.question_title,
            'q_tier': data.question.question_tier,
            'q_site': data.question.question_site
        } for data in datas]
        results[member.member_id] = result
        
    print(results)
        
    ## 이 페이지에서 보여줄 것
    context = {'title': 'Welcome to Baekjoon Crawling Results', 'results': results, 'time': update_time}
    return render(request, 'show_crawl_info/crawl_home.html', context)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated]

class SolveViewSet(viewsets.ModelViewSet):
    queryset = Solve.objects.all()
    serializer_class = SolveSerializer
    permission_classes = [permissions.IsAuthenticated]

        