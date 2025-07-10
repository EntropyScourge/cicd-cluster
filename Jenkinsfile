pipeline {
    agent any

    environment {
        def DOCKER_CREDENTIALS_ID = credentials('dockerhub-credentials')
        def SSH_CREDENTIALS_ID = credentials('azure-ssh-credentials')
        def CLUSTER_IP = credentials('cluster-ip-address')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                echo 'Building the app image...'
                sh 'cd app'
                docker.buildAndPush(
                    image: "entropyscourge/basic-fastapi-app:${env.BUILD_NUMBER}",
                    credentialsId: DOCKER_CREDENTIALS_ID,
                    registryUrl: 'https://index.docker.io/v1/',
                    dockerfile: 'Dockerfile'
                )
                echo 'Building the database image...'
                sh 'cd ../db'
                docker.buildAndPush(
                    image: "entropyscourge/app-db:${env.BUILD_NUMBER}",
                    credentialsId: DOCKER_CREDENTIALS_ID,
                    registryUrl: 'https://index.docker.io/v1/',
                    dockerfile: 'Dockerfile'
                )
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
                docker 'run -d --rm entropyscourge/basic-fastapi-app:latest'
                docker 'run -d --rm entropyscourge/app-db:latest'
                //curl 'http://localhost:8000/health' // Assuming the app exposes a health endpoint
                curl 'http://localhost:8000/posts'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                //ssh to remote server and deploy the application
                sshagent(credentials: [env.SSH_CREDENTIALS_ID]) {
                    sh '''
                    ssh -i ssh -i .ssh/app-cluster_key_2.pem azureuser@$CLUSTER_IP
                    docker pull entropyscourge/basic-fastapi-app:latest
                    docker pull entropyscourge/app-db:latest
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}