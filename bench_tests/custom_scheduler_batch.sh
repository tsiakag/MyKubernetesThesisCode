cd ../

# cluster specific values come from config.json in the repository root
CONTROL_PLANE_NODE=$(python3 -c 'import settings; print(settings.CONTROL_PLANE_NODE)')
echo "Starting bash script for netmarks scheduler testing"
echo "Time of start:"
date

# taint the control plane 
kubectl taint nodes "$CONTROL_PLANE_NODE" key1=value1:NoSchedule

for i in {1..24}
do
    echo "Iteration $i started..."

    # helm install
    cd ./my-robot-shop/K8s/helm_netmarks
    helm install robot-shop -n robot-shop .
    cd ../../..
    
    sleep 5s

    # run scheduler
    cd ./pod_scheduling_process
    python3 pod_scheduler.py $1
    cd ../

    sleep 1m

    # apply load
    kubectl apply -f ./my-robot-shop/K8s/load-deployment.yaml

    sleep 20m

    # get results
    cd ./bench_tests
    python3 write_results.py results/$2
    cd ../

    # delete application
    kubectl delete deploy load
    helm uninstall robot-shop

    sleep 20s

    echo "Iteration $i completed!"
    echo "---------------------------------------------------"
done

# untaint the control plane
kubectl taint nodes "$CONTROL_PLANE_NODE" key1=value1:NoSchedule-

echo "Netmarks Test Completed!"
echo "Ended at:"
date