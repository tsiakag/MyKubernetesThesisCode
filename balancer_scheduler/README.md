# Balancer Scheduler

Contains the required files to produce the bin balancer distribution of pods for scheduling. The Usage of each file:

- **fetch_opencost_costs**: Gets the required costs from a running kubernetes cluster for the algorithm to proccess later, and saves them in a JSON file. ***Note:*** Opencost **must** be running in the cluster and be port-forwarded in order for the script to work
- **bin_balancer**: Based on the costs json given, executes the bin balancer algorithm and produces the bin balancer distribution as JSON