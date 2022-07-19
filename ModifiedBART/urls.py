from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='bart-modified-home'),
    path('game/<str:trialId>', views.game, name='bart-modified-game'),
    path('cashOut/<str:trialId>', views.cashOut, name='bart-modified-cashOut'),

    path('example', views.example, name='bart-modified-example'),
    path('createExperiment', views.createExperiment, name='bart-modified-createExperiment'),
]
