# Pod Scheduling Process

Contains the script that schedules the pods taken from the imput distribution JSON to the corresponding nodes.<br>

In order to be used correctly, the pod yamls must be configured in a way that use a non-implemented kubernetes scheduler and during the deployment stay in the pending state.<br>

The script runs for about 2 minutes and can be used like this:

`python3 ./pod_scheduler.py <distribution>.json`