#USAGE:
# Was used to simply calculate the 
# differcences in % for the scheduler
# and be used in the thesis 
import os
import sys
# change directory of script so setting can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings

import numpy as np 
from matplotlib import pyplot as plt 
import pandas as pd

def calculate_percentage(x1, x2):
    if x1 > x2:
        return (1 - x1/x2) * 100
    else:
        return - (1 - x2/x1) * 100



def lists_to_dictionary(keys, values):
    return {keys[i]: values[i] for i in range(len(keys))}

apps = settings.APPS
df = pd.read_csv('./results_avg.csv')

# for array 
response_times = pd.DataFrame(df, columns=[app+'_ms' for app in apps])

# y = list(response_times.mean(axis=1)) 
y = list(df['average_cost_diff'])
x = list(df['scheduler']) 

d = lists_to_dictionary(x, y)

print(y)

for scheduler_base in d:
    print(f'{scheduler_base} compared to the others:')
    for scheduler_sec in d:
        print(f'{scheduler_sec}: {calculate_percentage(d[scheduler_base],d[scheduler_sec])}')
    print()

