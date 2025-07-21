# CI/CD Cluster

This repository comprises a simple CI/CD pipeline implemented through Jenkins, a two-tier web application built with Python and FastAPI, and Kubernetes configuration files for deploying the app on a Kubernetes cluster.

## Installation

- Clone the repository to an empty VM on a cloud platform of your choice
- Connect via SSH to the cluster VM
- Install Kubectl and Minikube and run `kubectl apply -f k8s` after starting Minikube, then `minikube service app-ip-service`
- Run `scripts/port-forward-loop.sh` as root to enable port forwarding to port 80
- Install Jenkins on another VM, and create a new pipeline which points to this repository on GitHub and its Jenkinsfile

You should now have a working cluster hosting the application, which will update automatically if any changes are pushed to the repository.