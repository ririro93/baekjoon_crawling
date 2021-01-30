from django.db import models

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
    ]
    
    SITE_CHOICES = [
        ('B', 'Baekjoon'),
        ('L', 'Leetcode'),
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
    
    def __str__(self):
        return self.member_id
    
class Solve(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    solved_time = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    