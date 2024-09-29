from django.urls import path, include
from rest_framework import routers
from .views import SurveyViewSet, QuestionViewSet, AnswerViewSet, UserParticipateViewSet


# Routers provide an easy way of automatically determining the URL conf.
surveys_router = routers.DefaultRouter()
surveys_router.register('', SurveyViewSet)
questions_router = routers.DefaultRouter()
questions_router.register('', QuestionViewSet)
answers_router = routers.DefaultRouter()
answers_router.register('', AnswerViewSet)
user_participate_router = routers.DefaultRouter()
user_participate_router.register('', UserParticipateViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('surveys/', include(surveys_router.urls)),
    path('questions/', include(questions_router.urls)),
    path('answers/', include(answers_router.urls)),
    path('user_participates/', include(user_participate_router.urls)),
]