from django.shortcuts import render
import plotly.express as px
from ModifiedBART.models import TrialModified
from StandardBART.models import Experiment, Trial
import pandas as pd

def home(request):
    trials = [[t['id']%10 if t['id']%10 != 0 else 10, t['experiment_id'], t['currentReward'], t['numPumps'], t['trialState']] for t in Trial.objects.all().values()]
    trialsModified = [[t['id']%10 if t['id']%10 != 0 else 10, t['experiment_id'], t['currentReward'], t['numPumps'], t['trialState']] for t in TrialModified.objects.all().values()]

    # TODO
    # (Possible point of upgrade)
    # ---------------------------
    # 1. instead of all trials at once, grab all experiments and order the trials in each experiment in ascending order, then visualize that.
    #   This is because some people might not finish an experimnet and multiple people might do experimnets at the same time, both situations 
    #   disrupt consecutive 1 - 10 trial IDs per experiment
    df1 = pd.DataFrame(data=trials, columns=['trialId', 'experimentId', 'currentReward', 'numPumps', 'trialState'])
    df1['currentReward'] = df1['currentReward'] + 0.1

    df2 = pd.DataFrame(data=trialsModified, columns=['trialId', 'experimentId', 'currentReward', 'numPumps', 'trialState'])
    df2['currentReward'] = df2['currentReward'] + 0.1

    
    fig1 = px.scatter(
        x=df1['trialId'], 
        y=df1['currentReward'],
        color=df1['trialId'], 
        title ="Distribution of Reward by Trials").update_layout(xaxis_title="Trial", yaxis_title="Reward for trial",
        )
    fig3 = px.scatter(
        x=df1['trialId'], 
        y=df1['numPumps'], 
        size=df1['currentReward'], 
        title ="Distribution of Number of pumps by Trials - Size based on Reward").update_layout(xaxis_title="Trial", yaxis_title="Number of pumps"
        )
    
    fig4 = px.scatter(
        x=df2['trialId'], 
        y=df2['currentReward'], 
        color=df2['trialId'], 
        title ="Distribution of Reward by Trials").update_layout(xaxis_title="Trial", yaxis_title="Reward for trial"
        )
    fig6 = px.scatter(
        x=df2['trialId'], 
        y=df2['numPumps'], 
        size=df2['currentReward'],
        title ="Distribution of Number of pumps by Trials - Size based on Reward").update_layout(xaxis_title="Trial", yaxis_title="Number of pumps"
        )

    context = {
        'fig1Learning' : fig1.to_html(),
        'fig3RiskDistribution' : fig3.to_html(),

        'fig4Learning' : fig4.to_html(),
        'fig6RiskDistribution' : fig6.to_html(),
    }

    return render(request, 'Landing/home.html', context)

def about(request):
    return render(request, 'Landing/about.html')