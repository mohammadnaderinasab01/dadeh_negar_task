from django.contrib import admin
from .models import Answer, Question, Survey, UserParticipate


admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserParticipate)