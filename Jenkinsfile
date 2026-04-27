pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/SatyasaiA99/python-devops-project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t python-devops-app .'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker stop python-app || true
                docker rm python-app || true
                docker run -d -p 5000:5000 --name python-app python-devops-app
                '''
            }
        }

        stage('Verify') {
            steps {
                sh '''
                sleep 5
                curl http://localhost:5000
                '''
            }
        }
    }
}
