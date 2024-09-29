from rest_framework import serializers
from surveys.models import Survey, Question, Answer, UserParticipate


class AnswerReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        depth = 1

class AnswerReadSerializerRequest(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        depth = 1

class AnswerCreateOrUpdateOrDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class QuestionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        depth = 1

class QuestionReadSerializerRequest(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        depth = 1

class QuestionCreateOrUpdateOrDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = ('answers',)


class SurveyReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'
        depth = 1

class SurveyReadSerializerRequest(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'
        depth = 1

class SurveyCreateOrUpdateOrDeleteSerializer(serializers.ModelSerializer):
    questions = QuestionCreateOrUpdateOrDeleteSerializer(read_only=True, many=True)
    class Meta:
        model = Survey
        fields = '__all__'


class UserParticipateReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserParticipate
        fields = '__all__'
        depth = 1

class UserParticipateReadSerializerRequest(serializers.ModelSerializer):
    survey = SurveyReadSerializer()
    class Meta:
        model = UserParticipate
        fields = '__all__'
        depth = 1

class UserParticipateCreateOrUpdateOrDeleteSerializer(serializers.ModelSerializer):
    # survey = SurveyCreateOrUpdateOrDeleteSerializer()
    # questions = serializers.ListField(child=serializers.CharField())
    # answers = serializers.ListField(child=serializers.CharField())
    class Meta:
        model = UserParticipate
        fields = '__all__'