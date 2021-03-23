import time
import datetime
import json
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.template.loader import get_template
from rest_framework import viewsets
from rest_framework import permissions

from .models import Question, Member, Solve, Update_time
from .serializers import MemberSerializer, SolveSerializer
from .forms import QuestionForm
from modules.baekjoon_crawling import Baekjoon
from modules.solved import Solved
from modules.get_all_solves import AllSolves

# from celery.result import AsyncResult
# from django_celery_beat.models import PeriodicTask, CrontabSchedule

# global variables
m_attrs = ['member_id', 'member_name']
q_attrs = ['question_title', 'question_number', 'question_site', 'question_tier']

############################################################# Celery Scheduler
# schedule, _ = CrontabSchedule.objects.get_or_create(
#     minute='*'
# )

# PeriodicTask.objects.get_or_create(
#     crontab=schedule,
#     name='background_crawling',
#     task='show_crawl_info.tasks.background_crawling'
# )

############################################################# Views

# db에 있는 최신 멤버랑 문제 정보 간략하게 보여주기
def crawl_home(request):
    print('crawl:', request)
    
    # 마지막 업데이트 된 시간 나중에 제대로 넣어보고 일단은 지금 시간 보내기
    formatted_updated_time, _ = get_formatted_updated_time()

    # db에서 오늘 문제 풀이 현황 불러오기
    results, formatted_start_date = get_prob_info('day', timezone.now())
    
    # 반환: 오늘 푼 문제들 리스트와 마지막으로 업데이트 된 시간
    context = {'results': results, 'updated_time': formatted_updated_time, 'start_date': formatted_start_date, 'page': 'details'}
    
    return render(request, 'show_crawl_info/crawl_home.html', context)

# 버튼 누르면 실행 될 부분
def refresh_button(request):
    req = json.loads(request.POST.get('data'))
    print('refresh', req)
    
    # get data
    button = req.get('button')
    update = req.get('update')
    search_date = req.get('search_date')
    search_year = int(search_date[:4])
    search_month = int(search_date[5:7])
    search_day = int(search_date[8:])
    datetime_search_date = datetime.datetime(search_year, search_month, search_day)
    
    # get last crawled time
    formatted_updated_time, _ = get_formatted_updated_time()

    # refresh 를 누른 경우
    if update == 'true':
        # DB 업데이트 해주기
        # time.sleep(5)                   # for testing
        print(update_members())
        print(update_questions_and_solves())
        print(update_question_tiers())

        # update update time
        now = timezone.now()
        print(now)
        Update_time.objects.create(updated_time=now)
        print('last crawl time update to: ', now)
        
        # 1분 안에 크롤링 또 했으면 경고 메세지 -> 여기 버그 왠지 모르겠는데 여기서 끊겨버림
        if now.hour == int(formatted_updated_time[:2]) and now.minute - int(formatted_updated_time[3:5]) <= 1:
            messages.warning(request, '크롤링 쿨타임 1분! 너무 자주하면 백준한테 막혀요ㅋㅋ..(경험담)')
            
        # 새로운 마지막 크롤링 시간 새로 반영
        formatted_updated_time = get_time()

        # message
        messages.success(request, 'DB has been updated successfully!')
        
    # 각각 누른 버튼에 대한 db 정보 가져오기
    if button == 'day':
        results, formatted_start_date = get_prob_info('day', datetime_search_date)
    elif button == 'week':
        results, formatted_start_date = get_prob_info('week', datetime_search_date)
    elif button == 'month':
        results, formatted_start_date = get_prob_info('month', datetime_search_date)
    elif button == 'total':
        results, formatted_start_date = get_prob_info('total', datetime_search_date)
    
    # ajax request 이니깐 messages 는 별도 처리
    django_messages = []

    for message in messages.get_messages(request):
        django_messages.append({
            "tag": message.level_tag,
            "message": message.message,
    })
        
    # 반환 : 최신화된 DB 정보랑 업데이트 한 지금 시간
    context = {'results': results, 'update_time': formatted_updated_time, 'start_date': formatted_start_date, 'messages': django_messages, 'page': 'details'}
    print('sending data to client')
    return HttpResponse(json.dumps(context), content_type='application/json')

# + 버튼 누르면 다른 사이트에서 푼 문제 추가 할 수 있도록
def add_question(request):
    form = QuestionForm(request.POST or None)
    context = {'form': form, 'page': 'add_solve'}
    if request.POST:
        if form.is_valid():
            data = form.cleaned_data
            print('valid form received: ')
            print(data)
            add_solve_to_db(data)
            messages.success(request, 'new solve submitted!')
            return HttpResponseRedirect(reverse('crawl-home'))
        else:
            messages.warning(request, 'please submit valid form!')
    return render(request, "show_crawl_info/add_question.html", context)

############################################################# DB update
# 최신 문제, 풀이 정보 업데이트 
def update_questions_and_solves():
    # get member ids
    member_ids = list(Member.objects.values_list('member_id', flat=True))
    
    # crawl those ids
    baek = Baekjoon()
    baek.initiate_multithread_crawling(member_ids)
    results = baek.get_member_solves_dict()
    
    # add new Questions and new Solves to db
    for member_id, solves in results.items():
        m = Member.objects.filter(member_id=member_id).first()
        for solve in solves:
            # get or create new Question objects, tier info not yet available
            q, q_bool = Question.objects.get_or_create(
                **{key: solve.get(key, '') for key in q_attrs[:-1]}
            )
            
            # update or create solves
            solved_time = solve['solved_time']
            formatted_solved_time = map(int, [solved_time[:4], solved_time[5:7], solved_time[8:10], solved_time[-8:-6], solved_time[-5:-3]])
            s, s_bool = Solve.objects.update_or_create(
                question=q,
                member=m,
                defaults={'solved_time': datetime.datetime(*formatted_solved_time)},
            )
    return 'questions and solves updated'

# 멤버 정보 업데이트
def update_members():
    new_members = []
    baek = Baekjoon()
    baek.crawl_member_ids()
    member_ids = baek.get_member_ids()
    for member_id in member_ids:
        m, m_bool = Member.objects.get_or_create(
            member_id=member_id
        )
        # if new get all past solves
        if m_bool:
            new_members.append(member_id)
            update_all_past_solves(member_id)
    if new_members:
        return f'{new_members} updated'
    else:
        return 'no new members'

# 티어 정보 업데이트
def update_question_tiers():
    # only questions with tier='' which was default
    q_nums_without_tier = list(Question.objects.filter(
        question_tier=''
        ).values_list('question_number', flat=True))
    
    # crawl tier info
    if q_nums_without_tier:
        solved = Solved(q_nums_without_tier)
        solved.initiate_multithread_crawling()
        tiers = solved.get_result() # [('4307', 'Silver II'), ...]
        
        # update Questions(백준문제만)
        for q_number, q_tier in tiers:
            Question.objects.filter(
                question_number=q_number,
                question_site='B',
            ).update(question_tier=q_tier)    
        return 'tiers updated'
    else:
        return 'no questions without tier info'

# db에 다른 사이트에서 푼 문제 추가하기
def add_solve_to_db(data):
    m, m_bool = Member.objects.get_or_create(
        member_id=data.get('member_id')
    )
    q, q_bool = Question.objects.get_or_create(
        **{key: data.get(key, '') for key in q_attrs}
    )    
    s, s_bool = Solve.objects.get_or_create(
        question=q,
        member=m,
        solved_time=data.get('solved_date') # 날짜까지만 받기 -> db에 midnight으로 저장됨
    )
    if m_bool:
        print('new Member added to db: ', data.get('member_id'))
    if q_bool:
        print('new Question added to db: ', (data.get('question_site'), data.get('question_number')))
    if s_bool:
        print('new Solve added to db')
    # 문제나 풀이가 생성되지 않았다만 디버깅 위해 프린트
    if not m_bool and not q_bool and not s_bool:
        print('######')
        print('data not added to db for some reason')

# 특정 멤버만 모든 문제 업데이트
def refresh_member(request, *args, **kwargs):
    print('## refreshing data for', kwargs.get('member_id'))
    update_all_past_solves(kwargs.get('member_id'))
    messages.info(request, f'{kwargs.get("member_id")} 문제 업데이트 완료')
    return HttpResponse(json.dumps({'data': 'success'}), content_type='application/json')
    
# 멤버가 푼 모든 문제 업데이트
def update_all_past_solves(member_id):
    # # delete all existing solves
    # former_solves = Solve.objects.filter(member=m)
    # for solve in former_solves:
    #     solve.delete()
    # print(f'## {member_id}\'s solves deleted')

    # get all past solves
    allsolves = AllSolves(member_id)
    allsolves.multi_threading()
    solves = allsolves.get_result()
    
    # make new solves
    m = Member.objects.get(member_id=member_id)
    for solve in solves:
        # get or create new Question objects, tier info not available yet
        q, q_bool = Question.objects.get_or_create(
            **{key: solve.get(key, '') for key in q_attrs[:-1]}
        )
        
        # update or create solves
        solved_time = solve['solved_time']
        formatted_solved_time = map(int, [solved_time[:4], solved_time[5:7], solved_time[8:10], solved_time[-8:-6], solved_time[-5:-3]])
        s, s_bool = Solve.objects.update_or_create(
            question=q,
            member=m,
            defaults={'solved_time': datetime.datetime(*formatted_solved_time)},
        )
    return f'{member_id} past solves updated'
            
############################################################ 여러 함수들
# 현재 시각 스트링으로 변환해서 반환
def get_time():
    # django.utils.timezone.now() 사용해서 서버에서도 한국시간 반영
    now = timezone.now()
    formatted_time = f'{now.hour:02}:{now.minute:02}:{now.second:02}'
    return formatted_time

# 마지막 크롤링 한 시간 스트링으로 변환해서 반환
def get_formatted_updated_time():
    u_times = Update_time.objects.all()
    if u_times:
        last_updated_time = u_times.first().updated_time
        last_updater = u_times.first().updater
        formatted_updated_time = f'{last_updated_time.hour:02}:{last_updated_time.minute:02}:{last_updated_time.second:02}'
        return formatted_updated_time, last_updater
    # db에 데이터 없는 경우 dummy data 반환
    else:
        return get_time(), 0

# 각 멤버가 오늘 푼 문제 정보 반환
def get_prob_info(time, datetime_search_date):
    # last_update_time을 어떻게 저장할지 생각해보기 -> global 시간 변수 사용?
    results = {}
    members = Member.objects.all()
    
    # db 비어있는 경우 대비
    formatted_start_date = get_time()
    
    for member in members:
        datas, formatted_start_date = member.get_member_solves(time, datetime_search_date)
        result = [{
            'q_num':data.question.question_number,
            'q_title':data.question.question_title,
            'q_tier': data.question.question_tier,
            'q_site': data.question.question_site
        } for data in datas]
        results[member.member_id] = result
    
    return results, formatted_start_date

############################################################# Django REST Framework
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated]

class SolveViewSet(viewsets.ModelViewSet):
    queryset = Solve.objects.all()
    serializer_class = SolveSerializer
    permission_classes = [permissions.IsAuthenticated]
    
############################################################ legacy code
# # DB 업데이트 해주는 함수
# def update_db():
#     ## init
#     keys_for_Question = (
#         'question_number',
#         'question_site',
#         'question_tier',
#         'question_title',
#     )
    
#     ## 최신 정보를 크롤링해서 db에 저장하기
#     # modules.baekjoon_crawling.py 사용
#     baek = Baekjoon()
#     results = baek.get_all_results()

#     # 여기 있는 if-else 다 get_or_create으로 없앨 수 있다?!
#     for member_id, questions in results.items():
#         # 멤버가 db에 있으면
#         if Member.objects.filter(member_id=member_id).exists():
#             m = Member.objects.get(member_id=member_id)
#         # 멤버 db에 없으면 생성하고 저장
#         else:
#             m = Member(member_id=member_id)
#             m.save()
        
#         ### 여기 느려서 손 봐야됨
#         # update questions (solved time정보는 빼고 넣기)
#         # questions가 최신께 앞에 들어있어서 전에 푼 시간이 최근에 푼 시간을 덮어씌움
#         # -> 역행하도록 설정 -> 나중엔 역행안하고 그냥 푼시간이 더 빠르면 저장안하는식으로 해도될듯
#         for question in questions[::-1]:
#             # 문제가 db에 있으면 그걸 멤버에 연결
#             if Question.objects.filter(question_number=question['question_number']).exists():
#                 q = Question.objects.get(question_number=question['question_number'])
#             # db에 해당 문제 추가 -> 첨 크롤링할 때 속성 더 가져와야됨 아예 결과도 dictionary 형태로 가져와보기
#             else:
#                 q = Question(**{key: question[key] for key in keys_for_Question})
#                 q.save()
#             # get date info and add to Solve
#             solved_time = question['solved_time']
#             formatted_solved_time = map(int, [solved_time[:4], solved_time[5:7], solved_time[8:10], solved_time[-8:-6], solved_time[-5:-3]])
            
#             # 이 사람이 과거에 이 문제 푼적있으면 업데이트 없으면 생성
#             solve, created_bool = Solve.objects.update_or_create(
#                 question=q,
#                 member=m,
#                 defaults={'solved_time': datetime.datetime(*formatted_solved_time)},
#             )
#             solve.save()  
#     return 'DB updated'