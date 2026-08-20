import os
import sys
# change directory of script so setting can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings

from matplotlib import pyplot as plt 
import pandas as pd

apps = settings.APPS
df = pd.read_csv('./all_response_and_balance.csv')

# show response time plots
for app in apps:
    y = list(df[app+'_ms']) 
    x = list(df['scheduler']) 
    
    plt.title("Average response time of " + app +' application') 
    plt.xlabel("scheduler") 
    plt.ylabel("response time (ms)") 
    plt.plot(x,y) 
    plt.grid()
    # plt.show()
    plt.savefig(f'../result_plots2_images(changed_labels)/{app}_response_time_plot.png')
    plt.clf()

# show average cost diff
y = list(df['average_cost_diff']) 
x = list(df['scheduler']) 

plt.title("Average cost balance of nodes") 
plt.xlabel("scheduler") 
plt.ylabel("Cost balance ($)") 
plt.plot(x,y)
plt.grid()
# plt.show()
plt.savefig(f'../result_plots2_images(changed_labels)/cost_balance_plot.png')
plt.clf()


# average whole app response time
response_times = pd.DataFrame(df, columns=[app+'_ms' for app in apps])

y = list(response_times.mean(axis=1)) 
x = list(df['scheduler']) 

plt.title("Average response time of whole installation(average of apps)") 
plt.xlabel("scheduler") 
plt.ylabel("response time (ms)") 
plt.plot(x,y) 
plt.grid()
# plt.show()
plt.savefig(f'../result_plots2_images(changed_labels)/application_response_plot.png')
plt.clf()
