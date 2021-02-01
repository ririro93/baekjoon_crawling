from django.db import models
import datetime

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
    ]
    
    SITE_CHOICES = [
        ('B', 'Baekjoon'),
        ('L', 'Leetcode'),
        ('P', 'Programmers'),
    ]
    
    question_title = models.CharField(default='제목 넣어줘..', max_length=100)
    question_number = models.CharField(default='번호 넣어줘..', max_length=100)
    question_tier = models.CharField(
        max_length=200,
        choices = TIER_CHOICES,
        default='B5'
    )

    question_site = models.CharField(
        max_length=200,
        choices = SITE_CHOICES,
        default='B'
    )
        
    def __str__(self):
        return self.question_number

class Member(models.Model):
    member_id = models.CharField(max_length=200)
    member_name = models.CharField(max_length=200, null=True, blank=True)
    member_solves = models.ManyToManyField(Question, through='Solve')
    
    def get_member_solves(self):
        return ', '.join([str(question) for question in self.member_solves.all()])
    
    
    # 일, 주, 월, 총 푼 문제 반환 -> 얘 잘 맞는지는 다른 요일에 다시 확인해보기
    def get_member_solves(self, time):
        if time == 'day':
            dday = 0
        elif time == 'week':
            # 월: 0, 일: 6
            dday = datetime.date.today().weekday()
        elif time == 'month':
            # 1일 이면 0 되게
            dday = datetime.date.today().day - 1
        else:
            # 대충 큰 수 빼기
            dday = 10000
        date = datetime.date.today() - datetime.timedelta(days=dday)
        solves = Solve.objects.filter(
            member__member_id=self.member_id,
            solved_time__gte=date
        )
        return solves
    
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
    