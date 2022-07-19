from distutils.dep_util import newer
import random
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Experiment, Trial

INFLATION_FACTOR = 3

def home(request):
    return render(request, 'StandardBART/home.html')

def example(request):
    return render(request, 'StandardBART/example.html')

def game(request, trialId):
    # TODO
    # (Possible point of upgrade)
    # ---------------------------
    # 1. Instead of sending every pump request to the server, use JavaScript to manipulate the size and perform removing numbers at random
    #   and only send request to the server when the balloon pops or player cashes out
    trial = Trial.objects.get(id=trialId)

    # check end of experiment to avoid players clicking back button and pumping again
    if trial.experiment.numCompletedTrials >= trial.experiment.totalTrials:
        return render(None, 'experimentCompleted.html', {'totalReward' : Trial.objects.get(id=trialId).experiment.totalCollected})

    context = {
        'trial' : trial,
        'balloonSize' : (10 + int(trial.numPumps))*INFLATION_FACTOR
    }

    return render(request, 'StandardBART/game.html', context=context)

    
def createExperiment(request):
    # create experiment, avoid redirect-render cycle
    # create new ecperiment and a trial with in that experiment
    newExperiment = Experiment.objects.create()
    newTrial = Trial.objects.create(experiment=newExperiment)

    return redirect(f'/standard-bart/game/{newTrial.id}')

def startTrial(trialId):
    # create new trial in an experiment
    trial = Trial.objects.get(id=trialId)
    newTrial = Trial.objects.create(experiment=Experiment.objects.get(id=trial.experiment.id))

    return newTrial

# pumping
def pumpOrPop(listOfNums):
    # remove numPumps number form listOfNums at random without replacement
    numAsStrList = [i.strip() for i in listOfNums[1:-1].split(',')] # change to list of ints becase what is passed is list as string
    numAsIntList = [int(i) for i in numAsStrList if i.isnumeric()]

    num = random.choice(numAsIntList)
    numAsIntList.remove(num)

    return ['pop', numAsIntList] if num==1 else ['_', numAsIntList]


def pump(request, trialId):    
    # called by the game template, avoid redirect-render cycle
    trial = Trial.objects.get(id=trialId)
    if trial.experiment.numCompletedTrials >= trial.experiment.totalTrials:
        return render(None, 'experimentCompleted.html', {'totalReward' : Trial.objects.get(id=trialId).experiment.totalCollected})


    trial.numPumps = int(trial.numPumps) + 1
    hasPopped, probList = pumpOrPop(trial.probList)

    if hasPopped == 'pop':
        trial.probList = str(probList)
        trial.trialState = 'state-pop'
        trial.currentReward = 0

        trial.experiment.lastCollected = 0
        trial.experiment.numCompletedTrials = int(trial.experiment.numCompletedTrials) + 1
        
        trial.experiment.save()
        trial.save()

        # check end of experiment to avoid players clicking back button and pumping again
        if trial.experiment.numCompletedTrials >= trial.experiment.totalTrials:
                return render(None, 'experimentCompleted.html', {'totalReward' : Trial.objects.get(id=trialId).experiment.totalCollected})
        else:
            newTrial = startTrial(trialId)

            return redirect(f'/standard-bart/game/{newTrial.id}')

    else:
        trial.probList = str(probList)
        trial.trialState = 'state-pump'
        trial.currentReward = float(trial.currentReward) + float(trial.experiment.rewardPerPump)
        
        trial.save()

        return redirect(f'/standard-bart/game/{trial.id}')

# cashing out
def cashOut(request, trialId):
    trial = Trial.objects.get(id=trialId)

    if trial.experiment.numCompletedTrials >= trial.experiment.totalTrials:
        return render(None, 'experimentCompleted.html', {'totalReward' : Trial.objects.get(id=trialId).experiment.totalCollected})

    trial.trialState = 'state-cash-out'
    trial.experiment.totalCollected = float(trial.experiment.totalCollected) + float(trial.currentReward)
    trial.experiment.lastCollected = float(trial.currentReward)
    
    trial.experiment.numCompletedTrials = int(trial.experiment.numCompletedTrials) + 1
    
    trial.experiment.save()
    trial.save()

    # check end of experiment to avoid players clicking back button and pumping again
    if trial.experiment.numCompletedTrials >= trial.experiment.totalTrials:
        return render(None, 'experimentCompleted.html', {'totalReward' : Trial.objects.get(id=trialId).experiment.totalCollected})
    else:
        newTrial = startTrial(trialId)

        return redirect(f'/standard-bart/game/{newTrial.id}')