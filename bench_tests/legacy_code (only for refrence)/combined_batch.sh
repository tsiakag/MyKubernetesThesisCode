cd ../
echo "Starting bash script for combined scheduler testing"
echo "Time of start:"
date

# taint the control plane 
kubectl taint nodes microk8s-tsiakag-control-plane-4gw82 key1=value1:NoSchedule

for i in {1..1}
do
    echo "Iteration $i started..."

    # helm install
    cd ./my-robot-shop/K8s/helm_netmarks
    helm install robot-shop -n robot-shop .
    cd ../../..
    
    sleep 5s

    # run scheduler
    cd ./combined_scheduler
    python3 produce_combined_distribution.py
    # cp ./netmarks_dist.json ./distributions/dist_$i.json
    python3 pod_scheduler.py
    cd ../

    sleep 1m

    # apply load
    kubectl apply -f ./my-robot-shop/K8s/load-deployment.yaml

    sleep 20m

    # get results
    cd ./bench_tests
    python3 write_results.py find_best_limit.csv
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

echo "Combined Test Completed!"
echo "Ended at:"
date