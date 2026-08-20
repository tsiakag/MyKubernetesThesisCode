#IMPORTANT NOTE:
# this script defines the scheduler by providing the json
# the bash scripts will have to specify this
import os
import sys
# change directory of script so setting can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings
from helper import connect_to_api, get_pod_appname, read_results

import time
import json

from kubernetes import client, watch
import warnings
warnings.filterwarnings("ignore") 

#region helper functions
v1 = connect_to_api()

scheduler_name = settings.SCHEDULER_NAME


def scheduler(name, node, namespace=settings.NAMESPACE):
        
    target=client.V1ObjectReference()
    target.kind="Node"
    target.apiVersion="v1"
    target.name= node
    
    meta=client.V1ObjectMeta()
    meta.name=name
    
    body=client.V1Binding(target=target)
    body.target = target
    body.metadata=meta
    
    try:
        return v1.create_namespaced_pod_binding(name, namespace, body)
    except:
        return

#endregion

def main():
    # read results
    data = read_results(sys.argv[1]) # change depending the way we want to schedule

    print('Naive scheduler is running...')
    tic = time.perf_counter()
    w = watch.Watch()
    # can change later watcable stream
    for event in w.stream(v1.list_namespaced_pod, settings.NAMESPACE):
        if event['object'].status.phase == "Pending" and event['object'].spec.scheduler_name == scheduler_name:
            # for testing purposes
            time.sleep(1)
            try:
                # res = scheduler(event['object'].metadata.name, scheduling_algorithm(event['object'].metadata.name, nodes_available(), True, 'robot-shop'))
                res = scheduler(event['object'].metadata.name, data[get_pod_appname(event['object'].metadata.name)])
            except client.rest.ApiException as e:
                print(json.loads(e.body)['message'])
            
            print(f'{event["object"].metadata.name} was scheduled!')
            print('-----------------------------------------------')

        if(time.perf_counter() - tic > 60): # due to being stuck in an eternal loop, we want to stop it after 1 min that all will be scheduled
            exit()
                    
if __name__ == '__main__':
    main()
