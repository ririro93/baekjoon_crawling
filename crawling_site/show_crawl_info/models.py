from django.db import models

class Question(models.Model):
    TIER_CHOICES = [
        ('B5', 'Bronze 5'),
        ('B4', 'Bronze 4'),
        ('B3', 'Bronze 3'),
        ('B2', 'Bronze 2'),
        ('B1', 'Bronze 1'),
        ('S5', 'Silver 5'),
        ('S4', 'Silver 4'),
        ('S3', 'Silver 3'),
        ('S2', 'Silver 2'),
        ('S1', 'Silver 1'),
        ('G5', 'Gold 5'),
        ('G4', 'Gold 4'),
        ('G3', 'Gold 3'),
        ('G2', 'Gold 2'),
        ('G1', 'Gold 1'),
        ('P5', 'Platinum 5'),
        ('P4', 'Platinum 4'),
        ('P3', 'Platinum 3'),
        ('P2', 'Platinum 2'),
        ('P1', 'Platinum 1'),
        ('D5', 'Diamond 5'),
        ('D4', 'Diamond 4'),
        ('D3', 'Diamond 3'),
        ('D2', 'Diamond 2'),
        ('D1', 'Diamond 1'),
        ('R5', 'Ruby 5'),
        ('R4', 'Ruby 4'),
        ('R3', 'Ruby 3'),
        ('R2', 'Ruby 2'),
        ('R1', 'Ruby 1'),
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H', 'Hard'),
    ]
    
    SITE_CHOICES = [
        ('B', 'Baekjoon'),
        ('L', 'Leetcode'),
    ]
    
    question_title = models.CharField(default='knapsack', max_length=200)
    question_number = models.IntegerField(default=0)
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
        return self.question_title

class Member(models.Model):
    member_id = models.CharField(max_length=200)
    member_name = models.CharField(max_length=200)
    member_solved = models.ManyToManyField(Question)
    
    def __str__(self):
        return self.member_name
    