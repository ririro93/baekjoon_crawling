from django import forms

class QuestionForm(forms.Form):
    member_id = forms.CharField(label='your id', max_length=100)
    question_site = forms.CharField(label='which site?')