# Single source of truth for the cluster specific values used by every script:
# node names, the namespace, the scheduler name, the app list and the
# Prometheus / OpenCost endpoints.
#
# The values themselves live in config.json next to this file, so moving the
# scripts to a different cluster only means editing that one JSON file.
#
# Scripts are run from inside their own folder (see bench_tests/*.sh), so they
# put the repository root on sys.path before importing this module:
#
#     import os
#     import sys
#     sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#     import settings
#
# NOTE: this module is called `settings` and not `config` on purpose. Most of
# the scripts already do `from kubernetes import client, config`, which would
# shadow a module named `config`.
import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

with open(CONFIG_PATH) as config_file:
    _config = json.load(config_file)

# region cluster
CONTROL_PLANE_NODE = _config['cluster']['control_plane_node']
WORKER_NODES = _config['cluster']['worker_nodes']
NAMESPACE = _config['cluster']['namespace']
SCHEDULER_NAME = _config['cluster']['scheduler_name']
# endregion

# region endpoints
PROMETHEUS_URL = _config['endpoints']['prometheus_url']
OPENCOST_URL = _config['endpoints']['opencost_url']
OPENCOST_ALLOCATION_URL = OPENCOST_URL + '/allocation/compute'
# endregion

# the robot-shop apps that are measured, in the order used by the plots
APPS = _config['workload']['apps']

# the cost columns written by bench_tests/write_results.py, control plane excluded
WORKER_NODE_COST_COLUMNS = [node + '_cost' for node in WORKER_NODES]
