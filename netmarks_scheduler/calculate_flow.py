# from netmarks import *
from prometheus_queries import FScore
from kubernetes import client, config, utils
from prometheus_api_client.utils import parse_datetime
import json

def connect_to_api():
    # server implementation
    config.load_kube_config()

    return client.CoreV1Api()

def list_pods(namespace='george'):
        apiInstance = connect_to_api()
        pods = apiInstance.list_namespaced_pod(namespace)

        podList = []
        for item in pods.items:
            podList.append(item.metadata.name)

        return podList

def get_pod_appname(pod):
    apiInstance = connect_to_api()
    pods = apiInstance.list_pod_for_all_namespaces()
    for item in pods.items:
        if item.metadata.name == pod:
            return item.metadata.labels['app']

def write_results_to_file(filename, results):
    # Serializing json
    json_object = json.dumps(results)
    
    # Writing to sample.json
    with open(filename, "w") as outfile:
        outfile.write(json_object)

# returns dict with flows between all apps
def calculate_all_flows():
    
    pods = list_pods('robot-shop')
    flows = {}

    for pod_x in pods:
        for pod_y in pods:
            
            if pod_x == pod_y:
                continue
            app_x = get_pod_appname(pod_x)
            app_y = get_pod_appname(pod_y)
            print(f'Calculating {app_x}->{app_y}')

            try:
                flows[app_x + '->' + app_y] = FScore(app_x, app_y, parse_datetime("1h"), 60)
            except:
                flows[app_x + '->' + app_y] = 0
            print('Completed\n')

    return flows


# NOTE:
# this file is used to calculate the Netmarks flows
# it uses the prometheus_queries methods to make the calculations
if __name__ == '__main__':

    res = calculate_all_flows()
    write_results_to_file('flows.json', res)
    print('Done')