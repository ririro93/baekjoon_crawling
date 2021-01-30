from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Member, Solve

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['member_id', 'member_name', 'member_solves']

        
class SolveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solve
        fields = ['question', 'member', 'solved_time']
        

