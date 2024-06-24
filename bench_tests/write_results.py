import os
import requests
import csv
from prometheus_api_client import PrometheusConnect
from prometheus_api_client.utils import parse_datetime
import sys

if __name__ == '__main__':
    
    # get the response times for each app
    apps = ['shipping', 'web', 'payment', 'cart', 'catalogue', 'ratings', 'user']
    
    ms_results = {}
    for app in apps:

        query = "sum(rate(istio_request_duration_milliseconds_sum{reporter='destination', destination_service='"+app+".robot-shop.svc.cluster.local'}[2m])) / sum(rate(istio_request_duration_milliseconds_count{reporter='destination', destination_service='"+app+".robot-shop.svc.cluster.local'}[2m]))"
        time_start = parse_datetime('15m')
        time_end = parse_datetime('now')

        prom = PrometheusConnect(url="http://localhost:9090", disable_ssl=True)
        metrics = prom.custom_query_range(query, time_start, parse_datetime('now'), '30s')

        # calculate the average response time
        # we count due to missing values
        accum = 0
        count = 0
        
        # if no metrics are present then we get an error, so write NaN
        try:
            for point in metrics[0]['values']:
                if point[1] != 'NaN':
                    accum += float(point[1])
                    count += 1

            if count != 0:
                ms_results[app+'_ms'] = accum / count
            else:
                ms_results[app+'_ms'] = 'NaN'
        
        except:
            ms_results[app+'_ms'] = 'NaN'

    # get costs
    parameters = {
        'window' : '15m',
        'step' : '2m',
        'resolution' : '1m',
        'aggregate' : 'node',
        'accumulate' : 'true'
    }

    res = requests.get('http://localhost:9003/allocation/compute', params=parameters).json()

    node_costs = {}

    for node, node_data in res['data'][0].items():
        node_costs[node+'_cost'] = node_data['totalCost']

    # some bug with the API I suppose
    if node_costs.__contains__('_cost'):
        node_costs.pop('_cost')

    # get the load cost
    parameters2 = {
        'window' : '15m',
        'step' : '2m',
        'resolution' : '1m',
        'aggregate' : 'pod',
        'accumulate' : 'true'
    }

    res = requests.get('http://localhost:9003/allocation/compute', params=parameters2).json()

    for pod, pod_data in res['data'][0].items():
        if pod.split('-')[0] == 'load':
            node_costs[pod_data['properties']['node']+'_cost'] -= float(pod_data['totalCost'])

    # write to csv file
    filename = sys.argv[1]
    with open(filename, 'a') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=ms_results.keys())
        
        ms_results.update(node_costs)

        # write fields if they do not exist
        if os.stat(filename).st_size == 0:
            temp = csv.writer(csvfile)
            temp.writerow(ms_results.keys())

        csvwriter.writerow(ms_results)
    
    print('Done writing results!')