#NOTE: 
# first arg: json distribution of pods -> nodes
# second arg: name of the csv that the results will be saved
cd ../
echo "Starting bash script for netmarks scheduler testing"
echo "Time of start:"
date

# taint the control plane 
kubectl taint nodes microk8s-tsiakag-control-plane-4gw82 key1=value1:NoSchedule

for i in {1..24}
do
    echo "Iteration $i started..."

    # helm install
    cd ./my-robot-shop/K8s/helm_netmarks
    helm install robot-shop -n robot-shop .
    cd ../../..
    
    sleep 5s

    # run scheduler
    cd ./netmarks_scheduler
    # python3 produce_netmarks_distribution.py
    # cp ./netmarks_dist.json ./distributions/dist_$i.json
    python3 pod_scheduler.py
    cd ../

    sleep 1m

    # apply load
    kubectl apply -f ./my-robot-shop/K8s/load-deployment.yaml

    sleep 20m

    # get results
    cd ./bench_tests
    python3 write_results.py netmarks_results_dist_6.csv
    cd ../

    # delete application
    kubectl delete deploy load
    helm uninstall robot-shop

    sleep 20s

    echo "Iteration $1 completed!"
    echo "---------------------------------------------------"
done

# untaint the control plane
kubectl taint nodes microk8s-tsiakag-control-plane-4gw82 key1=value1:NoSchedule-

echo "Netmarks Test Completed!"
echo "Ended at:"
date