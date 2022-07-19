import imp
from django.contrib import admin
from .models import Experiment, Trial

admin.site.register(Experiment)
admin.site.register(Trial)