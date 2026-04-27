pipeline {
    agent any

    environment {
        IMAGE_NAME = "python-devops-app"
        CONTAINER_NAME = "python-app"
        PORT = "5000"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/SatyasaiA99/python-devops-project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Stop Old Container') {
            steps {
                sh "docker stop ${CONTAINER_NAME} || true"
                sh "docker rm ${CONTAINER_NAME} || true"
            }
        }

        stage('Run Container') {
            steps {
                sh """
                docker run -d -p 5000:5000 --name python-app python-devops-app
                """
            }
        }

        stage('Verify') {
            steps {
                sh """
                sleep 5
                curl http://localhost:5000
                """
            }
        }
    }
}
