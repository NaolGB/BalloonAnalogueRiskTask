import imp
from django.contrib import admin
from .models import ExperimentModified, Pumps, TrialModified

admin.site.register(ExperimentModified)
admin.site.register(TrialModified)
admin.site.register(Pumps)