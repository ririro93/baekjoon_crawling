from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Member, Solve

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

        
class SolveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solve
        fields = '__all__'
        depth = 1

