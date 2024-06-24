import json
import binpacking
from kubernetes import client, config
import sys
from fetch_opencost_costs import write_results_to_file
import copy

def connect_to_api():
    config.load_kube_config()

    return client.CoreV1Api()

def nodes_available():
    v1 = connect_to_api()
    ready_nodes = []
    for n in v1.list_node().items:
            for status in n.status.conditions:
                if status.status == "True" and status.type == "Ready":
                    ready_nodes.append(n.metadata.name)
    return ready_nodes

def read_results(filename):
    # Opening JSON file
    f = open(filename)  
    data = json.load(f)
    f.close()

    return data

#NOTE:  main recursive algortihm
def my_distributer(dist, dist_apps ,index, weights, apps):

    # base case
    if index == len(weights):
        return dist, dist_apps
    
    # score keeps the absolute diffrence between the nodes
    best_score = float('inf')
    # result is the best distribution
    result = []
    # keep the best dist in apps
    results_apps = []

    # for each portion(node) add the object
    for portion in range(len(dist)):
        # new_dist = copy.deepcopy(dist)
        new_dist = dist.copy()
        new_dist[portion] += weights[index]

        new_dist_apps = copy.deepcopy(dist_apps) # deep copy is extremely slow
        # new_dist_apps = dist_apps.copy()
        new_dist_apps[portion].append(apps[index])

        best_dist, best_dist_apps = my_distributer(new_dist, new_dist_apps, index+1, weights, apps)

        # chose the dist with the least difference in weights using max - min / avg
        avg = sum(best_dist) / len(best_dist)
        score = (max(best_dist) - min(best_dist)) / avg

        # check if we got the minimum score
        if score < best_score:
            result = best_dist
            best_score = score
            results_apps = best_dist_apps

    return result, results_apps


if __name__ == '__main__':

    # read node_costs and remove unecessary pods
    existing_weights = dict(read_results('./node_costs.json'))
    existing_weights.pop('microk8s-tsiakag-control-plane-4gw82')
    existing_weights.pop('') # sometimes and empty record will appear

    existing_weights_list = list(existing_weights.values())

    # read container costs
    container_costs = dict(read_results('./pod_costs.json'))
    costs = {}
    for app, cost in container_costs.items():
        costs[app] = float(cost['totalCost'])
    costs.pop('load')
    
    # sort the costs and extract apps and weight values
    sorted_costs = dict(sorted(costs.items(), key=lambda x:x[1], reverse=True))
    apps = list(sorted_costs.keys())
    weights = list(sorted_costs.values())

    dist_apps = [ [] for _ in range(len(existing_weights_list))]

    # calculate the distribution
    score, result_apps = my_distributer(existing_weights_list, dist_apps, 0, weights, apps)

    # create the dist dictionary
    dist = {}
    for i in range(len(result_apps)):
        node = list(existing_weights.keys())[i]
        
        for app in result_apps[i]:
            dist[app] = node

    write_results_to_file('cost_dist.json', dist)


