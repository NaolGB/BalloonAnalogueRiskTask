import random
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import ExperimentModified, TrialModified, Pumps
from .forms import PumpsForm
from django.contrib import messages

INFLATION_FACTOR = 3 # the factor the balloon increases by per pump

def home(request):
    return render(request, 'ModifiedBART/home.html')

def example(request):
    return render(request, 'ModifiedBART/example.html')

def game(request, trialId):
    # TODO
    # (Possible point of upgrade)
    # ---------------------------
    # 1. Instead of sending every pump request to the server, use JavaScript to manipulate the size and perform removing numbers at random
    #   and only send request to the server when the balloon pops or player cashes out
    trial = TrialModified.objects.get(id=trialId)

    # check end of experiment to avoid players clicking back button and pumping again
    if trial.experiment.numCompletedTrials >= trial.experiment.totalTrials:
        return render(None, 'experimentCompleted.html', {'totalReward' : TrialModified.objects.get(id=trialId).experiment.totalCollected})

    context = {
        'trial' : trial,
        'balloonSize' : (10 + int(trial.numPumps))*INFLATION_FACTOR, # added 10 so that at the start of the trial the balloon with trial.numPumps = 0 can be seen with size (10+0)*INFLATION_FACTOR
        'form' : PumpsForm,
        'remainingPumps' : 128 - trial.numPumps
    }

    if request.method == 'POST':
        form = PumpsForm(request.POST)
        if(form.is_valid()):
            numPumps = int(form.cleaned_data['numPumps'])

            # check for valid number of pumps
            if(numPumps > (128 - trial.numPumps)) or numPumps <= 0:
                messages.error(request, 'Please insert number of pumps greater than zero (0) and less than or equal to the remaining number of pumps pumps.')
                return render(request, 'ModifiedBART/game.html', context)
            else:
                # send to another function, avoid redirect-render cycle
                return pump(request, numPumps=numPumps, trialId=trialId)

    return render(request, 'ModifiedBART/game.html', context)
    
def createExperiment(request):
    # create new ecperiment and a trial with in that experiment
    # create experiment, avoid redirect-render cycle
    newExperiment = ExperimentModified.objects.create()
    newTrial = TrialModified.objects.create(experiment=newExperiment)
    pumps = Pumps.objects.create(trial=newTrial)

    return redirect(f'/modified-bart/game/{newTrial.id}')

def startTrial(trialId):
    # create new trial in an experiment
    trial = TrialModified.objects.get(id=trialId)
    newTrial = TrialModified.objects.create(experiment=ExperimentModified.objects.get(id=trial.experiment.id))
    pumps = Pumps.objects.create(trial=newTrial)

    return newTrial

# pumping
def pumpOrPop(listOfNums, numPumps):
    # remove numPumps number form listOfNums at random without replacement
    numAsStrList = [i.strip() for i in listOfNums[1:-1].split(',')] # change to list of ints becase what is passed is list as string
    numAsIntList = [int(i) for i in numAsStrList if i.isnumeric()]

    for i in range(numPumps):
        num = random.choice(numAsIntList)
        if num == 1:
            return ['pop', i, numAsIntList]
        numAsIntList.remove(num)

    return ['_', i, numAsIntList]

def pump(request, numPumps, trialId):    
    trial = TrialModified.objects.get(id=trialId)
    pumpsModel = Pumps.objects.get(trial=trial)
    
    hasPopped, popIndex, probList  = pumpOrPop(trial.probList, numPumps)

    trial.numPumps = int(trial.numPumps) + numPumps
    pumpsModel.pumps = pumpsModel.pumps + ', ' + str(popIndex+1)
    pumpsModel.save()

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
            return render(None, 'experimentCompleted.html', {'totalReward' : TrialModified.objects.get(id=trialId).experiment.totalCollected})
        else:
            newTrial = startTrial(trialId)

            return redirect(f'/modified-bart/game/{newTrial.id}')

    else:
        trial.probList = str(probList)
        trial.trialState = 'state-pump'
        trial.currentReward = float(trial.currentReward) + (float(trial.experiment.rewardPerPump) * (popIndex + 1))
    
        trial.save()
        
        trial = TrialModified.objects.get(id=trialId)
        return redirect(f'/modified-bart/game/{trial.id}')

# cashing out
def cashOut(request, trialId):
    trial = TrialModified.objects.get(id=trialId)

    if trial.experiment.numCompletedTrials >= trial.experiment.totalTrials:
        return render(request, 'experimentCompleted.html')
    
    trial.trialState = 'state-cash-out'
    trial.experiment.totalCollected = float(trial.experiment.totalCollected) + float(trial.currentReward)
    trial.experiment.lastCollected = float(trial.currentReward)
    
    trial.experiment.numCompletedTrials = int(trial.experiment.numCompletedTrials) + 1
    
    trial.experiment.save()
    trial.save()
    
    # check end of experiment to avoid players clicking back button and pumping again
    if trial.experiment.numCompletedTrials >= trial.experiment.totalTrials:
        return render(None, 'experimentCompleted.html', {'totalReward' : TrialModified.objects.get(id=trialId).experiment.totalCollected})
    else:
        newTrial = startTrial(trialId)

        return redirect(f'/modified-bart/game/{newTrial.id}')

