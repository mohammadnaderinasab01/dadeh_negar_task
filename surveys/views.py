from rest_framework import status
# from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .serializer import SurveyCreateOrUpdateOrDeleteSerializer, SurveyReadSerializer, QuestionCreateOrUpdateOrDeleteSerializer, QuestionReadSerializer, AnswerCreateOrUpdateOrDeleteSerializer, AnswerReadSerializer, UserParticipateCreateOrUpdateOrDeleteSerializer, UserParticipateReadSerializer
# from shirts.models import CreatedShirt
from datetime import datetime
from .models import Survey, Question, Answer, UserParticipate
import numpy as np
import copy


class SurveyViewSet(GenericViewSet):
    queryset = Survey.objects.all()
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST' or self.request.method == 'PUT' or self.request.method == 'DELETE':
            return SurveyCreateOrUpdateOrDeleteSerializer
        elif self.request.method == 'GET':
            return SurveyReadSerializer
        return SurveyReadSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name='question_ids', type={'type': 'array', 'items': {'type': 'string'}},),
        ]
    )
    def create(self, request):
        # serializing the survey model
        try:
            int_result = np.array(request.GET.getlist('question_ids')).astype(int).tolist()

            questions = Survey.objects.filter(questions__id__in=int_result).values('questions')

            questions_ids = []
            create_data = copy.deepcopy(request.data)
            for question in questions:
                questions_ids.append(question['questions'])
            create_data['questions'] = questions_ids

            serializer = SurveyCreateOrUpdateOrDeleteSerializer(data=create_data)

            serializer.is_valid(raise_exception=True)
            serializer.save(questions=questions_ids)
            return Response({
                'validationMessage': [{
                    'statusCode': 201,
                    'message': 'اطلاعات با موفقیت ذخیره شد'
                }],
                'result': serializer.data,
                'resultStatus': 0
            }, status=201)
        except Exception as e:
            if type(e).__name__ == 'ValueError':
                return Response({
                    'validationMessage': [{
                        'statusCode': 400,
                        'message': 'تنها تایپ مورد قبول برای question_ids آرایه ای از اعداد است'
                    }],
                    'result': None,
                    'resultStatus': 1
                }, status=400)
            else:
                print(e)
                print(type(e))
                return Response({
                    'validationMessage': [{
                        'statusCode': 500,
                        'message': 'خطای ناشناخته'
                    }],
                    'result': None,
                    'resultStatus': 1
                }, status=500)


    def list(self, request):
        queryset = Survey.objects.all()

        serializer = SurveyReadSerializer(queryset, many=True)
        return Response({
                        'validationMessage': [{
                            'statusCode': 200,
                            'message': 'اطلاعات با موفقیت دریافت شد'
                        }],
                        'result': serializer.data,
                        'resultStatus': 0
                    }, status=200)


    def retrieve(self, request, pk):
        try:
            survey = Survey.objects.get(pk=pk)
            serializer = SurveyReadSerializer(instance=survey)
            return Response({
                        'validationMessage': [{
                            'statusCode': 200,
                            'message': 'اطلاعات با موفقیت دریافت شد'
                        }],
                        'result': serializer.data,
                        'resultStatus': 0
                    }, status=200)
        except Survey.DoesNotExist:
            return Response({
                        'validationMessage': [{
                            'statusCode': 404,
                            'message': 'اطلاعات یافت نشد'
                        }],
                        'result': None,
                        'resultStatus': 1
                    }, status=404)


    def update(self, request, pk):
        try:
            survey = Survey.objects.get(pk=pk)

            if request.data.get('title') != None and request.data['title'] != '':
                survey.title = request.data['title']

            if request.data.get('content') != None and request.data['content'] != '':
                survey.content = request.data['content']
            
            survey.save()
            serializer = SurveyCreateOrUpdateOrDeleteSerializer(instance=survey)
            return Response({
                        'validationMessage': [{
                            'statusCode': 202,
                            'message': 'اطلاعات با موفقیت بروزرسانی شد'
                        }],
                        'result': serializer.data,
                        'resultStatus': 0
                    }, status=202)
        except Survey.DoesNotExist:
            return Response({
                        'validationMessage': [{
                            'statusCode': 404,
                            'message': 'اطلاعات یافت نشد'
                        }],
                        'result': None,
                        'resultStatus': 1
                    }, status=404)


    def destroy(self, request, pk):
        try:
            survey = Survey.objects.get(pk=pk)
            serializer = SurveyCreateOrUpdateOrDeleteSerializer(instance=survey)
            survey.delete()
            return Response({
                        'validationMessage': [{
                            'statusCode': 204,
                            'message': 'اطلاعات با موفقیت حذف شد'
                        }],
                        'result': serializer.data,
                        'resultStatus': 0
                    }, status=204)
        except Survey.DoesNotExist:
            return Response({
                        'validationMessage': [{
                            'statusCode': 404,
                            'message': 'اطلاعات یافت نشد'
                        }],
                        'result': None,
                        'resultStatus': 1
                    }, status=404)


class QuestionViewSet(GenericViewSet):
    queryset = Question.objects.all()
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST' or self.request.method == 'PUT' or self.request.method == 'DELETE':
            return QuestionCreateOrUpdateOrDeleteSerializer
        elif self.request.method == 'GET':
            return QuestionReadSerializer
        return QuestionReadSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name='answer_ids', type={'type': 'array', 'items': {'type': 'string'}},),
        ]
    )
    def create(self, request):
        # serializing the question model
        try:
            int_result = np.array(request.GET.getlist('answer_ids')).astype(int).tolist()

            answers = Question.objects.filter(answers__id__in=int_result).values('answers')

            answers_ids = []
            create_data = copy.deepcopy(request.data)
            for answer in answers:
                answers_ids.append(answer['answers'])
            create_data['answers'] = answers_ids

            serializer = QuestionCreateOrUpdateOrDeleteSerializer(data=create_data)

            serializer.is_valid(raise_exception=True)
            serializer.save(answers=answers_ids)
            return Response({
                'validationMessage': [{
                    'statusCode': 201,
                    'message': 'اطلاعات با موفقیت ذخیره شد'
                }],
                'result': serializer.data,
                'resultStatus': 0
            }, status=201)
        except Exception as e:
            if type(e).__name__ == 'ValueError':
                return Response({
                    'validationMessage': [{
                        'statusCode': 400,
                        'message': 'تنها تایپ مورد قبول برای answer_ids آرایه ای از اعداد است'
                    }],
                    'result': None,
                    'resultStatus': 1
                }, status=400)
            else:
                return Response({
                    'validationMessage': [{
                        'statusCode': 500,
                        'message': 'خطای ناشناخته'
                    }],
                    'result': None,
                    'resultStatus': 1
                }, status=500)


    def list(self, request):
        queryset = Question.objects.all()

        serializer = QuestionReadSerializer(queryset, many=True)
        return Response({
            'validationMessage': [{
                'statusCode': 200,
                'message': 'اطلاعات با موفقیت دریافت شد'
            }],
            'result': serializer.data,
            'resultStatus': 0
        }, status=200)


    def retrieve(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
            serializer = QuestionReadSerializer(instance=question)
            return Response({
                'validationMessage': [{
                    'statusCode': 200,
                    'message': 'اطلاعات با موفقیت دریافت شد'
                }],
                'result': serializer.data,
                'resultStatus': 0
            }, status=200)
        except Question.DoesNotExist:
            return Response({
                'validationMessage': [{
                    'statusCode': 404,
                    'message': 'اطلاعات یافت نشد'
                }],
                'result': None,
                'resultStatus': 1
            }, status=404)


    def update(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)

            if request.data.get('title') != None and request.data['title'] != '':
                question.title = request.data['title']

            if request.data.get('content') != None and request.data['content'] != '':
                question.content = request.data['content']
            
            question.save()
            serializer = QuestionCreateOrUpdateOrDeleteSerializer(instance=question)
            return Response({
                'validationMessage': [{
                    'statusCode': 202,
                    'message': 'اطلاعات با موفقیت بروزرسانی شد'
                }],
                'result': serializer.data,
                'resultStatus': 0
            }, status=202)
        except Question.DoesNotExist:
            return Response({
                'validationMessage': [{
                    'statusCode': 404,
                    'message': 'اطلاعات یافت نشد'
                }],
                'result': None,
                'resultStatus': 1
            }, status=404)


    def destroy(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
            serializer = QuestionCreateOrUpdateOrDeleteSerializer(instance=question)
            question.delete()
            return Response({
                'validationMessage': [{
                    'statusCode': 204,
                    'message': 'اطلاعات با موفقیت حذف شد'
                }],
                'result': serializer.data,
                'resultStatus': 0
            }, status=204)
        except Question.DoesNotExist:
            return Response({
                'validationMessage': [{
                    'statusCode': 404,
                    'message': 'اطلاعات یافت نشد'
                }],
                'result': None,
                'resultStatus': 1
            }, status=404)


class AnswerViewSet(GenericViewSet):
    queryset = Answer.objects.all()
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST' or self.request.method == 'PUT' or self.request.method == 'DELETE':
            return AnswerCreateOrUpdateOrDeleteSerializer
        elif self.request.method == 'GET':
            return AnswerReadSerializer
        return AnswerReadSerializer


    def create(self, request):
        # serializing the question model
        serializer = AnswerCreateOrUpdateOrDeleteSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'validationMessage': [{
                'statusCode': 201,
                'message': 'اطلاعات با موفقیت ذخیره شد'
            }],
            'result': serializer.data,
            'resultStatus': 0
        }, status=201)


    def list(self, request):
        queryset = Answer.objects.all()

        serializer = AnswerReadSerializer(queryset, many=True)
        return Response({
            'validationMessage': [{
                'statusCode': 200,
                'message': 'اطلاعات با موفقیت دریافت شد'
            }],
            'result': serializer.data,
            'resultStatus': 0
        }, status=200)


    def retrieve(self, request, pk):
        try:
            question = Answer.objects.get(pk=pk)
            serializer = AnswerReadSerializer(instance=question)
            return Response({
                'validationMessage': [{
                    'statusCode': 200,
                    'message': 'اطلاعات با موفقیت دریافت شد'
                }],
                'result': serializer.data,
                'resultStatus': 0
            }, status=200)
        except Answer.DoesNotExist:
            return Response({
                'validationMessage': [{
                    'statusCode': 404,
                    'message': 'اطلاعات یافت نشد'
                }],
                'result': None,
                'resultStatus': 1
            }, status=404)


    def update(self, request, pk):
        try:
            question = Answer.objects.get(pk=pk)

            if request.data.get('title') != None and request.data['title'] != '':
                question.title = request.data['title']

            if request.data.get('value') != None and request.data['value'] != '':
                question.value = request.data['value']
            
            question.save()
            serializer = AnswerCreateOrUpdateOrDeleteSerializer(instance=question)
            return Response({
                'validationMessage': [{
                    'statusCode': 202,
                    'message': 'اطلاعات با موفقیت بروزرسانی شد'
                }],
                'result': serializer.data,
                'resultStatus': 0
            }, status=202)
        except Answer.DoesNotExist:
            return Response({
                'validationMessage': [{
                    'statusCode': 404,
                    'message': 'اطلاعات یافت نشد'
                }],
                'result': None,
                'resultStatus': 1
            }, status=404)


    def destroy(self, request, pk):
        try:
            question = Answer.objects.get(pk=pk)
            serializer = AnswerCreateOrUpdateOrDeleteSerializer(instance=question)
            question.delete()
            return Response({
                'validationMessage': [{
                    'statusCode': 204,
                    'message': 'اطلاعات با موفقیت حذف شد'
                }],
                'result': serializer.data,
                'resultStatus': 0
            }, status=204)
        except Answer.DoesNotExist:
            return Response({
                'validationMessage': [{
                    'statusCode': 404,
                    'message': 'اطلاعات یافت نشد'
                }],
                'result': None,
                'resultStatus': 1
            }, status=404)


class UserParticipateViewSet(GenericViewSet):
    queryset = UserParticipate.objects.all()
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST' or self.request.method == 'PUT' or self.request.method == 'DELETE':
            return UserParticipateCreateOrUpdateOrDeleteSerializer
        elif self.request.method == 'GET':
            return UserParticipateReadSerializer
        return UserParticipateReadSerializer


    def create(self, request):
        # serializing the user_participate model
        try:
            serializer = UserParticipateCreateOrUpdateOrDeleteSerializer(data=request.data)
            # print(request.data)
            survey_questions = Survey.objects.get(id=request.data.get('survey')).questions.all()
            survey_questions_identifier = 0
            selected_survey_question_answers_list = []
            survey_question_count = Survey.objects.get(id=request.data.get('survey')).questions.count()
            for survey_question in survey_questions:
                survey_question_answers = survey_question.answers.all()
                # print('survey_question_answers: ', survey_question_answers)
                if request.data.get('user_survey_question_answers') != None and len(request.data.get('user_survey_question_answers')) > 0:
                    if len(request.data.get('user_survey_question_answers')) < survey_question_count:
                        return Response({
                            'validationMessage': [{
                                'statusCode': 400,
                                'message': 'هنوز به تمام سوالات پاسخ نداده‌اید'
                            }],
                            'result': None,
                            'resultStatus': 1
                        }, status=400)
                    selected_survey_question_answer = survey_question_answers.get(value=request.data.get('user_survey_question_answers')[survey_questions_identifier])
                    selected_survey_question_answers_list.append(selected_survey_question_answer.value)
                    survey_questions_identifier += 1

            if len(selected_survey_question_answers_list) != survey_question_count:
                return Response({
                    'validationMessage': [{
                        'statusCode': 400,
                        'message': 'جواب تمام سوالات را با پاسخ‌های از پیش تعیین شده برای هر سوال پاسخ دهید'
                    }],
                    'result': None,
                    'resultStatus': 1
                }, status=400)
            serializer.is_valid(raise_exception=True)
            serializer.save(user_survey_question_answers=selected_survey_question_answers_list)
            return Response({
                'validationMessage': [{
                    'statusCode': 201,
                    'message': 'اطلاعات با موفقیت ذخیره شد'
                }],
                'result': serializer.data,
                'resultStatus': 0
            }, status=201)
        except Survey.DoesNotExist:
            return Response()
        except Answer.DoesNotExist:
            return Response({
                'validationMessage': [{
                    'statusCode': 400,
                    'message': 'جواب تمام سوالات را با پاسخ‌های از پیش تعیین شده برای هر سوال پاسخ دهید'
                }],
                'result': None,
                'resultStatus': 1
            }, status=400)


    def list(self, request):
        queryset = UserParticipate.objects.all()

        serializer = UserParticipateReadSerializer(queryset, many=True)
        return Response({
            'validationMessage': [{
                'statusCode': 200,
                'message': 'اطلاعات با موفقیت دریافت شد'
            }],
            'result': serializer.data,
            'resultStatus': 0
        }, status=200)


    def retrieve(self, request, pk):
        try:
            user_participate = UserParticipate.objects.get(pk=pk)
            serializer = UserParticipateReadSerializer(instance=user_participate)
            return Response({
                        'validationMessage': [{
                            'statusCode': 200,
                            'message': 'اطلاعات با موفقیت دریافت شد'
                        }],
                        'result': serializer.data,
                        'resultStatus': 0
                    }, status=200)
        except UserParticipate.DoesNotExist:
            return Response({
                        'validationMessage': [{
                            'statusCode': 404,
                            'message': 'اطلاعات یافت نشد'
                        }],
                        'result': None,
                        'resultStatus': 1
                    }, status=404)


    def destroy(self, request, pk):
        try:
            user_participate = UserParticipate.objects.get(pk=pk)
            serializer = UserParticipateCreateOrUpdateOrDeleteSerializer(instance=user_participate)
            user_participate.delete()
            return Response({
                        'validationMessage': [{
                            'statusCode': 204,
                            'message': 'اطلاعات با موفقیت حذف شد'
                        }],
                        'result': serializer.data,
                        'resultStatus': 0
                    }, status=204)
        except UserParticipate.DoesNotExist:
            return Response({
                        'validationMessage': [{
                            'statusCode': 404,
                            'message': 'اطلاعات یافت نشد'
                        }],
                        'result': None,
                        'resultStatus': 1
                    }, status=404)