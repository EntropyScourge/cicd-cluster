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
                        appImage.push("${env.BUILD_NUMBER}")
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
                        dbImage.push("${env.BUILD_NUMBER}")
                    }

                }
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
                script {
                    def appImage = docker.image("entropyscourge/basic-fastapi-app:${env.BUILD_NUMBER}")
                    def dbImage = docker.image("entropyscourge/app-db:${env.BUILD_NUMBER}")
                    dbImage.run('-p 5432:5432')
                    appImage.inside('-p 8000:8000') {
                        // Set environment variable for testing
                        sh '''
                        export ENV=TEST
                        pytest app/health_check.py
                        '''
                    }
                    dbImage.stop()
                }
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