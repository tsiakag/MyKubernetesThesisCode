# NETmarks Scheduler

Contains the scripts that use the NETmarks algorithm, creating a JSON distribution of pods. The scripts contained, have the following use:

- **prometheus_queries**: Contains definitions of prometheus queries in order to calculate the flow metric. ***Note:*** In order for the script to be executed, a ruuning instance of prometheus must be present in the Kubernetes cluster
- **calculate_flow**: Calculate the flows of all apps between them using the *prometheus_queries.py* script. It produces a JSON containg the flows between the apps
- **produce_netmarks_distribution**: Executes the main NETmarks algorithm, which produces a distribution JSON based on the inputed flows JSON