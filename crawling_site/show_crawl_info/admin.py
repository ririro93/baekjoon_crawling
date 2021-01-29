from django.contrib import admin

# Register your models here.
from .models import Member, Question

class MemberAdmin(admin.ModelAdmin):
    list_display = ('member_name', 'member_id')

class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'question_number', 
        'question_title', 
        'question_tier', 
        'question_site',
    )

admin.site.register(Member, MemberAdmin)
admin.site.register(Question, QuestionAdmin)
