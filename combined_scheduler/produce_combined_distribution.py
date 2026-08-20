import os
import sys
# change directory of script so setting can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings

from kubernetes import client, config, utils
import json


#region helper functions
def avg(x):
    return sum(x) / len(x)

def SetLimit(filename):
    with open(filename) as flows:
        data = json.load(flows)

        data = list(data.values())
        data = sorted(data, reverse=True)

        # remove zeros
        data = [el for el in data if el != 0]

        # keep the % of the biggest flows
        index = round(0.75 * len(data)) - 1

        # set the limit to this flow
        limit = data[index] - 1

        return limit

def connect_to_api():
    # server implementation
    config.load_kube_config()

    return client.CoreV1Api()

def nodes_available():
    ready_nodes = []
    for n in connect_to_api().list_node().items:
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

def get_pod_appname(pod):
    apiInstance = connect_to_api()
    pods = apiInstance.list_pod_for_all_namespaces()
    for item in pods.items:
        if item.metadata.name == pod:
            return item.metadata.labels['app']

def get_pod_namespace(pod):
    apiInstance = connect_to_api()
    pods = apiInstance.list_pod_for_all_namespaces()
    for item in pods.items:
        if item.metadata.name == pod:
            return item.metadata.namespace

def write_results_to_file(filename, results):
    # Serializing json
    json_object = json.dumps(results)
    
    # Writing to sample.json
    with open(filename, "w") as outfile:
        outfile.write(json_object)

def get_flows(filename):
    res = read_results(filename)
    flows = {}

    for key, val in res.items():
        app_x = key.split('->')[0]
        app_y = key.split('->')[1]
        
        flows[(app_x, app_y)] = int(val)

    return flows

def get_apps(flows):
    apps = set()

    for key in flows:
        apps.add(key[0])
        apps.add(key[1])

    return apps

def neighbors(app_x, State, flows):
    res = []

    for app in State:
        if(app != app_x):
            if((flows[(app_x, app)] != 0) or (flows[(app, app_x)] != 0)):
                res.append(app)

    return res

#endregion

# made it work with app instead of pods
def netmarks_algorithm(app_main, apps, nodes, dist, flows):
    # init scores to 0 for each node
    score = {}
    for node in nodes:
        score[node] = 0

    # iterate all nodes and get score
    for node in nodes:

        State = [app for app, n in dist.items() if n == node]
        Stats = neighbors(app_main, apps, flows)

        # for all common apps betweeen state and Stats
        for x in State:
            for y in Stats:

                if x == y: 
                    score[node] += (flows[(app_main, x)] + flows[(x, app_main)])

    # return node with max score aquired
    if max(score.values()) == 0:
        return dist[app_main]
    return max(score, key=score.get)


if __name__ == '__main__':

    # init values needed
    flows = get_flows('flows.json')
    nodes = nodes_available()
    nodes.remove(settings.CONTROL_PLANE_NODE) # remove the control plane node
    apps = list(get_apps(flows))

    # unlike netmarks, we use the balancer dist
    dist = dict(read_results('path to balancer dist'))

    # limit for combined algorithm
    limit = SetLimit('flows.json')

    # run algorithm for all apps
    for app in apps:

        # check the limit and then run netmark
        app_flow = sum([flows[(app, x)] for x in apps if x != app])
        if(app_flow > limit):
            print('in')
            res = netmarks_algorithm(app, apps, nodes, dist, flows)
            dist[app] = res
    
    print('--------------------------------------')
    print('The Combined distribution produced is:')
    for key, val in dist.items():
        print(key + " : " + val)
    print('--------------------------------------')


    # save data for deployment
    write_results_to_file('combined_dist.json', dist)