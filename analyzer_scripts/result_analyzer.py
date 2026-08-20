#USAGE:
# analyze the results from the csv's in order to
# create a csv that can be used for the plots

import os
import sys
# change directory of script so setting can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings
from helper import write_dict_row_to_csv

import pandas as pd


if __name__ == "__main__":
    results = {}
    # change it every time to desired
    filename = './combined_results.csv'
    # change it to desired
    results['scheduler'] = 'netmarks'

    apps = settings.APPS

    df = pd.read_csv(filename)

    # average of ms
    for app in apps:
        results[app+"_ms"] = df[app+"_ms"].mean()

    # we exclude the control plane
    # FIXME: change it to take the nodes from the API
    nodes_cols = settings.WORKER_NODE_COST_COLUMNS
    costs = pd.DataFrame(df, columns=nodes_cols)

    average_cost_diff = 0
    for index, row in costs.iterrows():
        if not (pd.isna(max(row)) and pd.isna(min(row))):
            average_cost_diff += max(row) - min(row)

            print(max(row) - min(row))

    print(df[nodes_cols[0]].size - 1)

    results['average_cost_diff'] = average_cost_diff / (df[nodes_cols[0]].size)
    print(results['average_cost_diff'])

    write_dict_row_to_csv(results, './results_avg.csv')

    print('Done!')
