import os
import sys
# change directory of script so setting can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings

from prometheus_api_client import PrometheusConnect
from datetime import timedelta, datetime
from prometheus_api_client.utils import parse_datetime

# establish prometheus connection
prom = PrometheusConnect(url=settings.PROMETHEUS_URL, disable_ssl=True)

def CalculateF(t_end, F_prev, t0, t1, labels, sample_rate):

    # passed the end time so we stop the calculations
    if t1 >= t_end - sample_rate:
        return F_prev

    # calculate the first part of the equation
    part_1 = F_prev * (t1 - t0) / (t1 + sample_rate - t0)

    #region get metrics from prometheus
    # get metrics for part 2 of the equation
    metric_request_data = prom.get_metric_range_data(
        "istio_request_bytes_sum",
        label_config=labels,
        start_time=datetime.fromtimestamp(t1),
        end_time=datetime.fromtimestamp(t1 + sample_rate + timedelta(seconds=1).total_seconds())
    )

    # calcluate metric for response
    metric_response_data = prom.get_metric_range_data(
        "istio_response_bytes_sum",
        label_config=labels,
        start_time=datetime.fromtimestamp(t1),
        end_time=datetime.fromtimestamp(t1 + sample_rate + timedelta(seconds=1).total_seconds())
    )
    #endregion


    #region set the data fetched from prometheus
    # the variables below sum the values of all request and response bytes sum.
    # We want to include all types of requests and responses, not only 200 OK
    req_t1 = 0
    req_tnew = 0
    res_t1 = 0
    res_tnew = 0
    for metric in metric_request_data:
        req_t1 += float(metric['values'][0][1])
        req_tnew += float(metric['values'][-1][1])

    for metric in metric_response_data:
        res_t1 += float(metric['values'][0][1])
        res_tnew += float(metric['values'][-1][1])
    #endregion

    # calculate part2 of the equation
    part_2 = ((req_tnew - req_t1) + (res_tnew - res_t1)) / (t1 + sample_rate - t0)


    # get new F
    F_new = part_1 + part_2

    #call new iteration
    return CalculateF(t_end, F_new, t0, t1 + sample_rate, labels, sample_rate)


def FScore(app, destination_app, time_start, sample_rate=15):
    # NOTE: sample rate is used for the steps in the CalculateF (typeof int)

    # set the labels for the query
    labels = {}
    labels['app']=app
    labels['destination_app']=destination_app

    # get initial data
    metric_response_data_init = prom.get_metric_range_data(
        "istio_response_bytes_sum",
        label_config=labels,
        start_time=time_start,
        end_time=parse_datetime("now"),
    )
    # get start time
    t0 = metric_response_data_init[0]['values'][0][0]
    F0 = 0

    # run the calculation algorithm
    return CalculateF(parse_datetime("now").timestamp(), F0, t0, t0, labels, timedelta(seconds=sample_rate).total_seconds())


def CheckConnectivity(app, destination_app, time_start):
    
    # set the labels for the query
    labels = {}
    labels['app']=app
    labels['destination_app']=destination_app

    # try to get data in order tp check the connection
    try:
        metric_response_data_init = prom.get_metric_range_data(
            "istio_response_bytes_sum",
            label_config=labels,
            start_time=time_start,
            end_time=parse_datetime("now"),
        )
        # temp value to check if error
        x = metric_response_data_init[0]['values'][0][0]
    except:
        raise Exception('No connectivity between apps')
    

