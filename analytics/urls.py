from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns=[
    path('analytics-reports', views.analytics_stats, name='analytics')
]