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
    ('L', 'Leetcode'),
    ('P', 'Programmers'),
    ('H', 'HackerRank'),
    ('S', 'SWEA'),
]

# to use date input not text input for solved_date field
class DateInput(forms.DateInput):
    input_type = 'date'
    
class QuestionForm(forms.Form):  
    member_id = forms.CharField(
        required=True, 
        label='your id',
        max_length=100
    )
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
    question_title = forms.CharField(
        required=False,
        label='question name',
    )
    question_number = forms.IntegerField(
        required=False,
        label='question number',
        initial=0,
    )
    solved_date = forms.DateField(
        widget=DateInput,
        required=True, 
        label='solved date?',
        initial=datetime.date.today(),
    )
    