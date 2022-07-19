from cProfile import label
from django.forms import ModelForm
from .models import Pumps

class PumpsForm(ModelForm):
    class Meta:
        model = Pumps
        fields = ['numPumps']
        labels = {
            'numPumps': 'Number of pumps'
        }