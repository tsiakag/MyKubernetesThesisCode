cd ../
echo "Starting bash script for bin balancer scheduler testing"
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
    cd ./balancer_scheduler
    python3 pod_scheduler.py
    cd ../

    sleep 1m

    # apply load
    kubectl apply -f ./my-robot-shop/K8s/load-deployment.yaml

    sleep 20m

    # get results
    cd ./bench_tests
    python3 write_results.py bin_balancer_results.csv
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

echo "Bin Balancer Test Completed!"
echo "Ended at:"
date