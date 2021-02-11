from django.db import models
import datetime
from django.utils import timezone

class Question(models.Model):
    TIER_CHOICES = [
        ('Bronze V', 'Bronze V'),
        ('Bronze IV', 'Bronze IV'),
        ('Bronze III', 'Bronze III'),
        ('Bronze II', 'Bronze II'),
        ('Bronze I', 'Bronze I'),
        ('Silver V', 'Silver V'),
        ('Silver IV', 'Silver IV'),
        ('Silver III', 'Silver III'),
        ('Silver II', 'Silver II'),
        ('Silver I', 'Silver I'),
        ('Gold V', 'Gold V'),
        ('Gold IV', 'Gold IV'),
        ('Gold III', 'Gold III'),
        ('Gold II', 'Gold II'),
        ('Gold I', 'Gold I'),
        ('Platinum V', 'Platinum V'),
        ('Platinum IV', 'Platinum IV'),
        ('Platinum III', 'Platinum III'),
        ('Platinum II', 'Platinum II'),
        ('Platinum I', 'Platinum I'),
        ('Diamond V', 'Diamond V'),
        ('Diamond IV', 'Diamond IV'),
        ('Diamond III', 'Diamond III'),
        ('Diamond II', 'Diamond II'),
        ('Diamond I', 'Diamond I'),
        ('Ruby V', 'Ruby V'),
        ('Ruby IV', 'Ruby IV'),
        ('Ruby III', 'Ruby III'),
        ('Ruby II', 'Ruby II'),
        ('Ruby I', 'Ruby I'),
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H', 'Hard'),
        ('LEVEL 1', 'LEVEL 1'),
        ('LEVEL 2', 'LEVEL 2'),
        ('LEVEL 3', 'LEVEL 3'),
        ('LEVEL 4', 'LEVEL 4'),
        ('LEVEL 5', 'LEVEL 5'),
        ('D1', 'D1'),
        ('D2', 'D2'),
        ('D3', 'D3'),
        ('D4', 'D4'),
        ('D5', 'D5'),
        ('D6', 'D6'),
        ('D7', 'D7'),
        ('D8', 'D8'),
    ]
    
    SITE_CHOICES = [
        ('B', 'Baekjoon'),
        ('L', 'Leetcode'),
        ('P', 'Programmers'),
        ('H', 'HackerRank'),
        ('S', 'SWEA'),
    ]
    
    question_title = models.CharField(default='제목 넣어줘..', max_length=200)
    question_number = models.CharField(default='번호 넣어줘..', max_length=200, null=True)
    question_tier = models.CharField(
        max_length=200,
        choices = TIER_CHOICES,
        default=''
    )

    question_site = models.CharField(
        max_length=200,
        choices = SITE_CHOICES,
        default='B'
    )
    updated = models.DateTimeField(auto_now=True)

        
    def __str__(self):
        return self.question_number

class Member(models.Model):
    member_id = models.CharField(max_length=200)
    member_name = models.CharField(max_length=200, null=True, blank=True)
    member_solves = models.ManyToManyField(Question, through='Solve')
    
    def get_member_solved_probs(self):
        return ', '.join([str(question) for question in self.member_solves.all()])
    
    
    # 일, 주, 월, 총 푼 문제 반환 -> 얘 잘 맞는지는 다른 요일에 다시 확인해보기
    def get_member_solves(self, time, datetime_search_date):
        end_date = datetime_search_date + datetime.timedelta(days=1)
        if time == 'day':
            dday = 0
        elif time == 'week':
            dday = 6
        elif time == 'month':
            dday = 30
        else:
            # 대충 큰 수 빼기, total은 마지막 날이 무조건 오늘
            dday = 10000
            end_date = timezone.now() + datetime.timedelta(days=1)
        date = datetime_search_date - datetime.timedelta(days=dday)
        solves = Solve.objects.filter(
            member__member_id=self.member_id,
            solved_time__gte=date,
        ).exclude(
            solved_time__gte=end_date,
        )
        formatted_start_date = f'{date.year}-{date.month:02}-{date.day:02}'
        return solves, formatted_start_date
    
    def __str__(self):
        return self.member_id
    
class Solve(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    solved_time = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-solved_time']

    def __str__(self):
        return self.question.question_number

class Update_time(models.Model):
    updater = models.CharField(null=True, blank=True, max_length=100)
    updated_time = models.DateTimeField()
    
    class Meta:
        ordering = ['-updated_time']
        
    def __str__(self):
        return f'{self.updater} updated at {self.updated_time}'