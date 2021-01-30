from django.contrib import admin

# Register your models here.
from .models import Member, Question, Solve

class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'member_id', 
        'member_name', 
        'get_member_solves',
    )
    ## manytomany field 값인 get_member_solves 도 넣고 싶은데 안된데
    # fields = (
    #     'member_name', 
    #     'member_id', 
    #     'get_member_solves',
    # )

class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'question_number', 
        'question_title', 
        'question_tier', 
        'question_site',
    )
    
class SolveAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'question', 
        'member',
        'solved_time', 
        'updated',
    )
    

admin.site.register(Member, MemberAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Solve, SolveAdmin)
