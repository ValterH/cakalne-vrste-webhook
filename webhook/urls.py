from django.urls import path
from . import views

urlpatterns = [
    path('webhook/', views.webhook, name='webhook'),
    path('getProcedures/', views.get_procedures, name='procedures'),
    path('getUrgencies/', views.get_urgency, name='urgency'),
    path('getRegions/', views.get_regions, name='regions'),
    path('getWaitingTimes/<str:pro>/<str:urg>/<str:reg>', views.get_waiting_times, name='waiting times'),
    path('getWaitingTimes/<str:pro>/<str:urg>/', views.waiting_times_no_region, name='waiting times no region'),
    path('updateDatabase/', views.update_db, name='database')
    ]
