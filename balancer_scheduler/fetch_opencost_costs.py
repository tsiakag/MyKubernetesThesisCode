import json
import requests


def write_results_to_file(filename, results):
    # Serializing json
    json_object = json.dumps(results)
    
    # Writing to sample.json
    with open(filename, "w") as outfile:
        outfile.write(json_object)


if __name__ == '__main__':

    parameters = {
        'window' : '20h',
        'step' : '10m',
        'resolution' : '1m',
        'aggregate' : 'pod',
        'accumulate' : 'true'
    }
    
    res = requests.get('http://localhost:9003/allocation/compute', params=parameters).json()

    # check if the request was valid
    if res['code'] != 200:
       print('Invalid Request')
       exit()
    

    costs = {}
    for pod, pod_data in res['data'][0].items():
        app = pod.split('-')[0]
        if(pod_data['properties']['namespace'] == 'robot-shop'):
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
    node_res = requests.get('http://localhost:9003/allocation/compute', params=parameters).json()
    
    if res['code'] != 200:
       print('Invalid Request')
       exit()

    # calculate total cost
    node_costs = {}
    for node, node_data in node_res['data'][0].items():
        node_costs[node] = float(node_data['totalCost'])


    # then remove the robot-shop containers costs
    for pod, pod_data in res['data'][0].items():
        if(pod_data['properties']['namespace'] == 'robot-shop'):
            app = pod.split('-')[0]
            node = pod_data['properties']['node']

            node_costs[node] -= costs[app]['totalCost']

    write_results_to_file('node_costs.json', node_costs)

    print('Done')