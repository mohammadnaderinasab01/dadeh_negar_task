from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

class Answer(models.Model):
    title = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    def __str__(self):
        return self.title


class Question(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField(max_length=1000, blank=True, null=True)
    answers = models.ManyToManyField(Answer, blank=True, null=True)
    
    def __str__(self):
        return self.title


class Survey(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True, null=True)
    questions = models.ManyToManyField(Question, blank=True, null=True)
    
    def __str__(self):
        return self.title


class UserParticipate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participate_user')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='participate_user_survey')
    
    user_survey_question_answers = ArrayField(models.TextField(max_length=50), null=True, blank=True)
    
    def __str__(self):
        return self.survey.title