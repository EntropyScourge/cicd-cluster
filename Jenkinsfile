pipeline {
    agent any

    environment {
        // Define environment variables here if needed
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                echo 'Building the project...'
                // Add your build commands here, e.g.:
                // sh './gradlew build'
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
                // Add your test commands here, e.g.:
                // sh './gradlew test'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                // Add your deployment commands here
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