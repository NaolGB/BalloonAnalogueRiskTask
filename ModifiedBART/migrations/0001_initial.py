# Generated by Django 4.0.5 on 2022-11-13 21:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExperimentModified',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalTrials', models.IntegerField(default=10)),
                ('numCompletedTrials', models.IntegerField(default=0)),
                ('totalCollected', models.FloatField(default=0)),
                ('lastCollected', models.FloatField(default=0)),
                ('rewardPerPump', models.FloatField(default=0.5)),
                ('experimentType', models.CharField(default='modified', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='TrialModified',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balloonColor', models.CharField(default='Blue', max_length=32)),
                ('currentReward', models.FloatField(default=0)),
                ('numPumps', models.IntegerField(default=0)),
                ('trialState', models.CharField(default='state-start-from-cash-out', max_length=32)),
                ('probList', models.CharField(default=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128], max_length=1024)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ModifiedBART.experimentmodified')),
            ],
        ),
        migrations.CreateModel(
            name='Pumps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numPumps', models.PositiveIntegerField(default=1)),
                ('pumps', models.CharField(default='', max_length=1024)),
                ('trial', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ModifiedBART.trialmodified')),
            ],
        ),
    ]
