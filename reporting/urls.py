from django.urls import path, include
from rest_framework import routers
from .views import ReportingViewSet


# Routers provide an easy way of automatically determining the URL conf.
reportings_router = routers.DefaultRouter()
reportings_router.register('', ReportingViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('reportings/', include(reportings_router.urls)),
    path('nth_most_popular_surveys/', ReportingViewSet.as_view({'get': 'nth_most_popular_surveys'})),
]