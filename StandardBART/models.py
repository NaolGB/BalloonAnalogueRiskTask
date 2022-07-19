from django.db import models

class Experiment(models.Model):
    totalTrials = models.IntegerField(default=10)
    numCompletedTrials = models.IntegerField(default=0)
    totalCollected = models.FloatField(default=0)
    lastCollected = models.FloatField(default=0)
    rewardPerPump = models.FloatField(default=0.5)

    def __str__(self) -> str:
        return (f'{self.id}')


def createProbArray():
    return [i for i in range(1, 129)]
    
class Trial(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.PROTECT)
    numPumps = models.IntegerField(default=0)
    currentReward = models.FloatField(default=0)
    trialState = models.CharField(default='state-start-from-cash-out', max_length=32) # state-start-from-cash-out, state-pump, state-pop
    probList = models.CharField(default=createProbArray(), max_length=1024) # list of numbers [1 - 128] from which number are removed at random. If 1 is removed then the balloon pops
    

    def __str__(self) -> str:
        return (f'{self.id}')

