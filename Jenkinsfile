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
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        def appImage = docker.build(
                            "entropyscourge/basic-fastapi-app:${env.BUILD_NUMBER}",
                            "--build-arg BUILD_DATE=\$(date -u +'%Y-%m-%dT%H:%M:%SZ') " +
                            "--build-arg VCS_REF=\$(git rev-parse --short HEAD) " +
                            "--no-cache app"
                        )
                        appImage.tag("latest")
                        appImage.push("${env.BUILD_NUMBER}")
                        appImage.push("latest")
                    }
                }
                echo 'Building the database image...'
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        def dbImage = docker.build(
                            "entropyscourge/app-db:${env.BUILD_NUMBER}",
                            "--build-arg BUILD_DATE=\$(date -u +'%Y-%m-%dT%H:%M:%SZ') " +
                            "--build-arg VCS_REF=\$(git rev-parse --short HEAD) " +
                            "--no-cache db"
                        )
                        dbImage.tag("latest")
                        dbImage.push("${env.BUILD_NUMBER}")
                        dbImage.push("latest")
                    }

                }
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '''
                sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                sudo chmod +x /usr/local/bin/docker-compose
                sudo docker-compose -f docker-compose.yml up -d --build
                sudo docker-compose -f docker-compose.yml exec app pytest app/health_check.py
                sudo docker-compose -f docker-compose.yml down
                '''
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                //ssh to remote server and deploy the application
                sshagent(['azure-ssh-credentials']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no azureuser@${env.CLUSTER_IP}\\
                    cd cicd-cluster/ &&
                    kubectl set image k8s/app-deployment basic-fastapi-app=entropyscourge/basic-fastapi-app:${env.BUILD_NUMBER} &&
                    kubectl rollout status deployment/app-deployment &&
                    kubectl apply -f k8s
                    """
                }
            }
        }
    }

                    //kubectl set image k8s/app-deployment basic-fastapi-app=entropyscourge/basic-fastapi-app:${env.BUILD_NUMBER}\\
                    //kubectl set image k8s/postgres-deployment db=entropyscourge/app-db:${env.BUILD_NUMBER}\\

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