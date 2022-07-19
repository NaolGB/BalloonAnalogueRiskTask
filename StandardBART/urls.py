from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='bart-home'),
    path('example', views.example, name='bart-example'),
    path('game/<str:trialId>', views.game, name='bart-game'),
    path('createExperiment', views.createExperiment, name='bart-createExperiment'),

    path('pump/<str:trialId>', views.pump, name='bart-pump'),
    path('cashOut/<str:trialId>', views.cashOut, name='bart-cashOut'),

]
