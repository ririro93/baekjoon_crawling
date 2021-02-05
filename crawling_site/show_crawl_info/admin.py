from django.contrib import admin

# Register your models here.
from .models import Member, Question, Solve, Update_time

class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'member_id', 
        'member_name', 
        'get_member_solved_probs',
    )

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
    
class UpdateTimeAdmin(admin.ModelAdmin):
    list_display = (
        'updater',
        'updated_time',
    )
    
    

admin.site.register(Member, MemberAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Solve, SolveAdmin)
admin.site.register(Update_time, UpdateTimeAdmin)
