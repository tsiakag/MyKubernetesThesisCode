cd ../
echo "Starting bash script all schedulers testing"
echo "Time of start:"
date

# taint the control plane 
kubectl taint nodes microk8s-tsiakag-control-plane-4gw82 key1=value1:NoSchedule

# region original
echo "Original scheduler testing started..."
    
    # helm install
    cd ./my-robot-shop/K8s/helm
    helm install robot-shop -n robot-shop .
    cd ../../..

    #wait to init and run load
    sleep 1m

    # apply load
    kubectl apply -f ./my-robot-shop/K8s/load-deployment.yaml

    sleep 20m

    # get results
    cd ./bench_tests
    python3 write_results.py all_results4.csv
    cd ../

    # delete application
    kubectl delete deploy load
    helm uninstall robot-shop

    #wait for load to terminate
    sleep 20s
    echo "Original scheduler testing completed!"
    echo "---------------------------------------------------"
# endregion

# region netmarks (dist1)

echo "Netmarks testing started..."

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
    python3 write_results.py all_results4.csv
    cd ../

    # delete application
    kubectl delete deploy load
    helm uninstall robot-shop

    sleep 20s

    echo "Netmarks testing completed!"
    echo "---------------------------------------------------"

# endregion

# region opencost

echo "Opencost testing started..."

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
    python3 write_results.py all_results4.csv
    cd ../

    # delete application
    kubectl delete deploy load
    helm uninstall robot-shop

    sleep 20s

    echo "Opencost testing completed!"
    echo "---------------------------------------------------"

# endregion

# region Combined

echo "Combined testing started..."

    # helm install
    cd ./my-robot-shop/K8s/helm_netmarks
    helm install robot-shop -n robot-shop .
    cd ../../..
    
    sleep 5s

    # run scheduler
    cd ./combined_scheduler
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
    python3 write_results.py all_results4.csv
    cd ../

    # delete application
    kubectl delete deploy load
    helm uninstall robot-shop

    sleep 20s

    echo "Combined testing completed!"
    echo "---------------------------------------------------"

# endregion

# untaint the control plane
kubectl taint nodes microk8s-tsiakag-control-plane-4gw82 key1=value1:NoSchedule-

echo "All schedulers testing Completed!"
echo "Ended at:"
date