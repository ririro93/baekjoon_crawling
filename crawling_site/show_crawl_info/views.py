import time
import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.template.loader import get_template
from rest_framework import viewsets
from rest_framework import permissions

 
from show_crawl_info.models import Question, Member, Solve
from show_crawl_info.serializers import MemberSerializer, SolveSerializer

from modules.baekjoon_crawling import Baekjoon


# db에 있는 최신 멤버랑 문제 정보 간략하게 보여주기
def crawl_home(request):
    print('crawl:', request)
    
    # 마지막 업데이트 된 시간 나중에 제대로 넣어보고 일단은 지금 시간 보내기
    updated_time = get_time()
                    
    # db에서 오늘 문제 풀이 현황 불러오기
    results = get_prob_info('day')
    
    # 반환: 오늘 푼 문제들 리스트와 마지막으로 업데이트 된 시간
    context = {'results': results, 'time': updated_time}
    
    return render(request, 'show_crawl_info/crawl_home.html', context)


# 버튼 누르면 실행 될 부분
def refresh_button(request):
    req = json.loads(request.POST.get('data'))
    print('refresh', req)
    update = req.get('update')
    button = req.get('button')
    # reassign global updated_time
    updated_time = req.get('last_updated_time')
    
    ## refresh 를 누른 경우
    if update == 'true':
        # DB 업데이트 해주기
        print(update_db()) # 애니메이션 테스트 위해 잠시 중단
        # time.sleep(2)
        updated_time = get_time()
        
    # 각각 누른 버튼에 대한 db 정보 가져오기
    if button == 'day':
        results = get_prob_info('day')
    elif button == 'week':
        results = get_prob_info('week')
    elif button == 'month':
        results = get_prob_info('month')
    elif button == 'total':
        results = get_prob_info('total')
    
    # 반환 : 최신화된 DB 정보랑 업데이트 한 지금 시간
    context = {'results': results, 'update_time': updated_time}
    
    return HttpResponse(json.dumps(context), content_type='application/json')

# 현재 시각 스트링으로 변환해서 반환해주는 함수
def get_time():
    now = datetime.datetime.now()
    formatted_time = f'{now.hour:02}:{now.minute:02}:{now.second:02}'
    return formatted_time

# DB 업데이트 해주는 함수
def update_db():
    ## init
    keys_for_Question = (
        'question_number',
        'question_site',
        'question_tier',
        'question_title',
    )
    
    ## 최신 정보를 크롤링해서 db에 저장하기
    # modules.baekjoon_crawling.py 사용
    baek = Baekjoon()
    results = baek.get_all_results()

    # 여기 있는 if-else 다 create_of_get으로 없앨 수 있다?!
    for member_id, questions in results.items():
        # 멤버가 db에 있으면
        if Member.objects.filter(member_id=member_id).exists():
            m = Member.objects.get(member_id=member_id)
        # 멤버 db에 없으면 생성하고 저장
        else:
            m = Member(member_id=member_id)
            m.save()
        
        ### 여기 느려서 손 봐야됨
        # update questions (solved time정보는 빼고 넣기)
        # questions가 최신께 앞에 들어있어서 전에 푼 시간이 최근에 푼 시간을 덮어씌움
        # -> 역행하도록 설정 -> 나중엔 역행안하고 그냥 푼시간이 더 빠르면 저장안하는식으로 해도될듯
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
    return 'DB updated'


# 각 멤버가 오늘 푼 문제 정보 반환
def get_prob_info(time):
    # last_update_time을 어떻게 저장할지 생각해보기 -> global 시간 변수 사용?
    results = {}
    members = Member.objects.all()
    for member in members:
        datas = member.get_member_solves(time)
        result = [{
            'q_num':data.question.question_number,
            'q_title':data.question.question_title,
            'q_tier': data.question.question_tier,
            'q_site': data.question.question_site
        } for data in datas]
        results[member.member_id] = result
    return results



## Django REST Framework Test   
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated]

class SolveViewSet(viewsets.ModelViewSet):
    queryset = Solve.objects.all()
    serializer_class = SolveSerializer
    permission_classes = [permissions.IsAuthenticated]