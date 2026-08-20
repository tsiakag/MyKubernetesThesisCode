import os
import sys
# change directory of script so setting can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings
from helper import write_results_to_file

import requests


if __name__ == '__main__':

    parameters = {
        'window' : '20h',
        'step' : '10m',
        'resolution' : '1m',
        'aggregate' : 'pod',
        'accumulate' : 'true'
    }
    
    res = requests.get(settings.OPENCOST_ALLOCATION_URL, params=parameters).json()

    # check if the request was valid
    if res['code'] != 200:
       print('Invalid Request')
       exit()
    

    costs = {}
    for pod, pod_data in res['data'][0].items():
        app = pod.split('-')[0]
        if(pod_data['properties']['namespace'] == settings.NAMESPACE):
            costs[app] = {}

            costs[app]['cpu'] = pod_data['cpuCost']
            costs[app]['ram'] = pod_data['ramCost']
            costs[app]['pv'] = pod_data['pvCost']
            costs[app]['totalCost'] = pod_data['totalCost']

    write_results_to_file('pod_costs.json', costs)

    
    # calculate the nodes costs without the robot shop application
    parameters = {
        'window' : '20h',
        'step' : '10m',
        'resolution' : '1m',
        'aggregate' : 'node',
        'accumulate' : 'true'
    }
    node_res = requests.get(settings.OPENCOST_ALLOCATION_URL, params=parameters).json()
    
    if res['code'] != 200:
       print('Invalid Request')
       exit()

    # calculate total cost
    node_costs = {}
    for node, node_data in node_res['data'][0].items():
        node_costs[node] = float(node_data['totalCost'])


    # then remove the robot-shop containers costs
    for pod, pod_data in res['data'][0].items():
        if(pod_data['properties']['namespace'] == settings.NAMESPACE):
            app = pod.split('-')[0]
            node = pod_data['properties']['node']

            node_costs[node] -= costs[app]['totalCost']

    write_results_to_file('node_costs.json', node_costs)

    print('Done')