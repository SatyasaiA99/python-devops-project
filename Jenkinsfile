pipeline {
    agent any

    environment {
        APP_NAME = "python-devops-app"
        IMAGE_NAME = "satyasaia99/python-devops-app"
        IMAGE_TAG = "v1"

        SONARQUBE_ENV = "sq"

        DOCKERHUB_USER = "satyasaia99"
    }

    stages {

        /* ---------------- CHECKOUT ---------------- */
        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/SatyasaiA99/python-devops-project.git'
            }
        }

        /* ---------------- PYTHON INSTALL ---------------- */
        stage('Install Dependencies') {
            steps {
                sh '''
                python3 --version
                pip3 install -r requirements.txt
                '''
            }
        }

        /* ---------------- SONARQUBE ---------------- */
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${SONARQUBE_ENV}") {
                    sh 'mvn sonar:sonar'
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        /* ---------------- QUALITY GATE ---------------- */
        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        /* ---------------- DOCKER BUILD ---------------- */
        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                """
            }
        }

        /* ---------------- PUSH TO DOCKER HUB ---------------- */
        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'Dockerhub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh """
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }

        /* ---------------- RUN CONTAINER ---------------- */
        stage('Run Container') {
            steps {
                sh '''
                docker stop python-app || true
                docker rm python-app || true
                docker run -d -p 5000:5000 --name python-app python-devops-app:v1
                '''
            }
        }

        /* ---------------- VERIFY ---------------- */
        stage('Verify') {
            steps {
                sh '''
                sleep 5
                curl http://localhost:5000
                '''
            }
        }
    }

    post {
        success {
            echo "🚀 Python Pipeline Success"
        }
        failure {
            echo "❌ Python Pipeline Failed"
        }
    }
}
