from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .serializer import SurveyCreateOrUpdateOrDeleteSerializer, SurveyReadSerializer
from surveys.models import Survey, Question, Answer, UserParticipate
import numpy as np
import copy, json
from django.db.models import Count


class ReportingViewSet(GenericViewSet):
    queryset = Survey.objects.all()
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST' or self.request.method == 'PUT' or self.request.method == 'DELETE':
            return SurveyCreateOrUpdateOrDeleteSerializer
        elif self.request.method == 'GET':
            return SurveyReadSerializer
        return SurveyReadSerializer


    @extend_schema(
        parameters=[
            OpenApiParameter(name='number_of_records', type=OpenApiTypes.INT),
        ]
    )
    def nth_most_popular_surveys(self, request):
        try:
            n = request.GET.get('number_of_records', '10')
            queryset = UserParticipate.objects.values('survey__id', 'survey').annotate(count=Count('survey__id')).order_by('survey__id')[:int(n)]

            output_surveys = []
            for item in list(queryset):
                output_surveys.append(SurveyReadSerializer(Survey.objects.get(id=item['survey'])).data)

            return Response({
                'validationMessage': [{
                    'statusCode': 200,
                    'message': 'اطلاعات با موفقیت دریافت شد'
                }],
                'result': output_surveys,
                'resultStatus': 0
            }, status=200)
        except:
            return Response({
                'validationMessage': [{
                    'statusCode': 500,
                    'message': 'خطای ناشناخته'
                }],
                'result': None,
                'resultStatus': 1
            }, status=500)