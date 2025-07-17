#!/bin/bash

# This script continuously attempts to establish a port-forward to app cluster.
# It will restart the port-forward if it gets disconnected.
# It must be run on the machine hosting the app cluster.
# usage: sudo ./port-forward-loop.sh (sudo is required to bind to port 80)


while true; do
    echo "$(date): Starting port-forward to service/app-ip-service"
    kubectl port-forward --address 0.0.0.0 service/app-ip-service 80:80

    # If we get here, the port-forward died
    echo "$(date): Port-forward disconnected, restarting in 3 seconds..."
    sleep 3
done