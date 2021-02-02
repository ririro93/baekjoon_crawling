import datetime
from django import forms

TIER_CHOICES = [
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
    ('L', 'Leetcode'),
    ('P', 'Programmers'),
]

class QuestionForm(forms.Form):  
    member_id = forms.CharField(required=True, label='your id', max_length=100)
    question_site = forms.ChoiceField(
        required=True, 
        label='question site?',
        choices=SITE_CHOICES,
    )
    question_tier = forms.ChoiceField(
        required=True,
        label='difficulty',
        choices=TIER_CHOICES,
    )
    # not necessary if programmers
    question_number = forms.IntegerField(
        required=False,
        label='question number',
    )
    solved_date = forms.DateField(
        widget=forms.SelectDateWidget(),
        required=True, 
        label='solved date?',
        initial=datetime.date.today(),
    )