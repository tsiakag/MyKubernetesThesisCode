#USAGE:
# analyze the results from the csv's in order to
# create a csv that can be used for the plots

import pandas as pd
import csv
import sys

def write_to_csv(line, file):
    # write to csv file
    with open(file, 'a') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=line.keys())

        # write fields if they do not exist

        csvwriter.writerow(line)

if __name__ == "__main__":
    results = {}
    # change it every time to desired
    filename = './combined_results.csv'
    # change it to desired
    results['scheduler'] = 'netmarks'

    apps = ['shipping', 'web', 'payment', 'cart', 'catalogue', 'ratings', 'user']

    df = pd.read_csv(filename)

    # average of ms
    for app in apps:
        results[app+"_ms"] = df[app+"_ms"].mean()

    # we exclude the control plane
    # FIXME: change it to take the nodes from the API
    nodes_cols = ['microk8s-tsiakag-md-0-66rwq_cost','microk8s-tsiakag-md-0-9zd48_cost','microk8s-tsiakag-md-0-j2cfc_cost']
    costs = pd.DataFrame(df, columns=nodes_cols)

    average_cost_diff = 0
    for index, row in costs.iterrows():
        if not (pd.isna(max(row)) and pd.isna(min(row))):
            average_cost_diff += max(row) - min(row)

            print(max(row) - min(row))

    print(df[nodes_cols[0]].size - 1)

    results['average_cost_diff'] = average_cost_diff / (df[nodes_cols[0]].size)
    print(results['average_cost_diff'])

    write_to_csv(results, './results_avg.csv')

    print('Done!')


# TODO: remove ????
def analyze_scatter_plot(scheduler_name):
    results = {}
    # change it every time to desired
    filename = './analyze_for_scatter.csv'
    # change it to desired
    results['scheduler'] = scheduler_name

    apps = ['shipping', 'web', 'payment', 'cart', 'catalogue', 'ratings', 'user']


    df = pd.read_csv(filename)

    # average of ms
    for app in apps:
        results[app+"_ms"] = df[app+"_ms"].mean()

    # we exclude the control plane
    nodes_cols = ['microk8s-tsiakag-md-0-66rwq_cost','microk8s-tsiakag-md-0-9zd48_cost','microk8s-tsiakag-md-0-j2cfc_cost']
    costs = pd.DataFrame(df, columns=nodes_cols)

    average_cost_diff = 0
    for index, row in costs.iterrows():
        if not (pd.isna(max(row)) and pd.isna(min(row))):
            average_cost_diff += max(row) - min(row)

            print(max(row) - min(row))

    print(df[nodes_cols[0]].size - 1)

    results['average_cost_diff'] = average_cost_diff / (df[nodes_cols[0]].size)
    print(results['average_cost_diff'])

    write_to_csv(results, './all_response_and_balance.csv')