# Balloon Analogue Risk Tasj
Implementation of Balloon Analogue Risk Task (BART) using Django

### TODO
- [x] Setup Django environment
- [x] Implement standard BART and modified BART
- [x] Generate plotly visualizations
- [x] Style 
- [x] Deploy (CICD): https://www.bart.bynaol.com

## About
Balloon Analogue Risk Task (BART) is a computer game to measure risk taking behavior of players. It is used by researchers and employers to determine, among others, risk propensity. This repository of my implemetation of Balloon Analogue Rist Task (BART) using Djago. This implementaion provides collection of data in multiple ways. Collection for basic data points like number of pumps and rewards are already built in, however, the program is built to support implementaiton of recording for more data types, some metioned in the Current/Future Progress section. Currently live <a href="https://www.bart.bynaol.com/">on my website</a>. Read more <a href="https://www.bart.bynaol.com/about-bart">on the website's about page and more</a>


## Possible Points of Upgrade
These you can find with in the codes as comments. These are points of upgrade I imagined could better the program. These are suggestions, and also my focus as I improve this program.

## Visualization
Visualizations for this project are made in Plotly because of the easy embedding and interactivity offered by Plotly.

See the interactive visualizations <a href="https://www.bart.bynaol.com/">on my website</a>.

The non-interactive versionis given here for fast access

<strong>Standard BART</strong>
![BART Distribution of Number of pumps by Trials - Size based on Reward](images/BART-Distribution-of-Number-of-pumps-by-Trials.png)
This image shows distribution of number of pumps (inflations) per trial. The size is based on the reward recieved for that trial.


![BART distribution of rewards by trial](images/BART-Distribution-of-Rewards-by-Trial.png)
This image shows the distribution of rewards by trials. Color is based on the tial number.


<strong>Modified BART</strong>
![MBART Distribution of Number of pumps by Trials - Size based on Reward](images/MBART-Distribution-of-Number-of-pumps-by-Trials.png)
This image shows distribution of number of pumps (inflations) per trial. The size is based on the reward recieved for that trial.


![MBART - Distribution of Reward by Trials](images/MBART-Distribution-of-Reward-by-Trials.png)
This image shows the distribution of rewards by trials. Color is based on the tial number.


## Current/Future Progress
Currently, under this project, I am working on:
- creating methods to record more type of data including time to decesion and mouse movement
