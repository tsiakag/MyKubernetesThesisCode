# from netmarks import *
import os
import sys
# change directory of script so setting can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings
from helper import connect_to_api, get_pod_appname, write_results_to_file

from prometheus_queries import FScore
from prometheus_api_client.utils import parse_datetime

def list_pods(namespace=settings.NAMESPACE):
        apiInstance = connect_to_api()
        pods = apiInstance.list_namespaced_pod(namespace)

        podList = []
        for item in pods.items:
            podList.append(item.metadata.name)

        return podList


# returns dict with flows between all apps
def calculate_all_flows():
    
    pods = list_pods(settings.NAMESPACE)
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