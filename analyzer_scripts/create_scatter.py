import os
import sys
# change directory of script so setting can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings

import numpy as np 
from matplotlib import pyplot as plt 
import pandas as pd
import csv

def write_to_csv(line, file):
    # write to csv file
    with open(file, 'a') as csvfile:
        csvwriter = csv.writer(csvfile)

        # write fields if they do not exist
        csvwriter.writerow(line)
if __name__ == '__main__':
    files = [
        '../results/original_results.csv',
        '../results/netmarks_results_dist_1.csv',
        '../results/netmarks_results_dist_6.csv',
        '../results/bin_balancer_results.csv',
        '../results/combined_results.csv'
    ]

    colors=['k', 'm', 'r', 'g', 'b']
    labels=['original', 'netmarks1', 'netmarks6', 'bin balancer', 'combined']

    apps = settings.APPS

    for file in files:
        # use result_analyzer (slower but easier (i dont even care any more))

        # the list with the points
        x = list()
        y = list()
        # for each row find the points of the list 
        with open(file) as file_obj: 
      
            # Skips the heading 
            heading = next(file_obj)[:-1].split(",") # remove \n and then split it to a list

            # reading file 
            reader_obj = csv.reader(file_obj) 

            
            # write each row 
            for row in reader_obj:
                # last 3 elements are the cost that matter to us and the rest the response time
                # NOTE: we exclude the control-pane from the costs
                response_times = row[:-4]
                costs = row[-3:]
                costs = np.array(costs, dtype=float)

                line = [labels[files.index(file)], np.mean(np.array(response_times, dtype=float)), max(costs) - min(costs)]
                write_to_csv(line, 'analyze_for_scatter.csv')

                y.append(np.mean(np.array(response_times, dtype=float)))
                x.append(max(costs) - min(costs))

        print(x, y)
        color = colors[files.index(file)]
        label = labels[files.index(file)]
        plt.scatter(x, y, c=color, label=label)

    plt.title("Scatter plot average response time to cost balance")
    plt.ylabel("Response time (ms)")
    plt.xlabel("Cost Balance")
    plt.legend()
    plt.grid(True)
    plt.show()

    