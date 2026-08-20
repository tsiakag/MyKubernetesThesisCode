import csv
import json

from kubernetes import client, config

#region kubernetes
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

def get_pod_appname(pod):
    apiInstance = connect_to_api()
    pods = apiInstance.list_pod_for_all_namespaces()
    for item in pods.items:
        if item.metadata.name == pod:
            return item.metadata.labels['app']

#endregion

#region json files
def read_results(filename):
    # Opening JSON file
    f = open(filename)  
    data = json.load(f)
    f.close()

    return data

def write_results_to_file(filename, results):
    # Serializing json
    json_object = json.dumps(results)
    
    # Writing to sample.json
    with open(filename, "w") as outfile:
        outfile.write(json_object)
#endregion

#region netmarks flows
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

#region csv
def write_dict_row_to_csv(line, file):
    # write to csv file
    with open(file, 'a') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=line.keys())

        # write fields if they do not exist

        csvwriter.writerow(line)

def write_row_to_csv(line, file):
    # write to csv file
    with open(file, 'a') as csvfile:
        csvwriter = csv.writer(csvfile)

        # write fields if they do not exist
        csvwriter.writerow(line)
#endregion
