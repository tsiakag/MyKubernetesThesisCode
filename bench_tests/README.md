# Bench Tests

Contains the bash scripts that can be used for testing the cluster with the different distribution and stress tests them based on the [robot-shop](https://github.com/instana/robot-shop) application and load deployment. The files contained have the following uses:

- **write_results**: Python script that fetches the results of each test and writes them in an output csv in the results directory. It is used in all the bash scripts while being executed
- **custom_scheduler_batch**: Executes a testing procedure that deploys the pods of robot-shop, schedules them using pod_scheduler.py, generates load and after some time fetches the results and writes them to a csv, for a specified n times. Syntax: <br><br>
    `./custom_scheduler_batch.sh <distribution.json> <output.csv>` <br>

- **default_scheduler_batch**: Executes a testing procedure that deploys the pods of robot-shop using the default Kubernetes scheduler, generates load and after some time fetches the results and writes them to a csv, for a specified n times. Syntax: <br><br>
    `./default_scheduler_batch.sh <output.csv>` 