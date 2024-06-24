#NOTE: 
# first arg: name of the csv that the results will be saved
cd ../
echo "Starting bash script for default scheduler testing"
echo "Time of start:"
date

# taint the control plane 
kubectl taint nodes microk8s-tsiakag-control-plane-4gw82 key1=value1:NoSchedule

for i in {1..24}
do
    echo "Iteration $i started..."
    
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
    python3 write_results.py $1
    cd ../

    # delete application
    kubectl delete deploy load
    helm uninstall robot-shop

    #wait for load to terminate
    sleep 20s
    echo "Iteration $i completed!"
    echo "---------------------------------------------------"
done

# untaint the control plane
kubectl taint nodes microk8s-tsiakag-control-plane-4gw82 key1=value1:NoSchedule-

echo "Default Test Completed!"
echo "Ended at:"
date
