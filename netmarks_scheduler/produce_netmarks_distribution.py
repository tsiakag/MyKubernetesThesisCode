import os
import sys
# change directory of script so setting can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings
from helper import nodes_available, write_results_to_file, get_flows, get_apps, neighbors

import random


# NOTE: Main algorithm
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

    # create a random distribution of apps in the nodes
    dist = {}
    for app in apps:
        dist[app] = random.choice(nodes)

    # run algorithm for all apps
    for app in apps:
        res = netmarks_algorithm(app, apps, nodes, dist, flows)
        dist[app] = res
    print('--------------------------------------')
    print('The Netmarks distribution produced is:')
    for key, val in dist.items():
        print(key + " : " + val)
    print('--------------------------------------')


    # save data for deployment
    write_results_to_file('netmarks_dist.json', dist)