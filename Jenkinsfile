pipeline {
    agent any

    environment {
        APP_NAME = "python-devops-app"
        IMAGE_NAME = "satyasaia99/python-devops-app"
        IMAGE_TAG = "v1"

        SONARQUBE_ENV = "sq"

        NEXUS_URL = "http://13.206.85.161:8081"
        NEXUS_REPO = "python-repo"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/SatyasaiA99/python-devops-project.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 --version
                pip3 install -r requirements.txt
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${SONARQUBE_ENV}") {
                    sh '''
                    /opt/sonar-scanner/bin/sonar-scanner \
                    -Dsonar.projectKey=python-devops \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=$SONAR_HOST_URL \
                    -Dsonar.login=$SONAR_AUTH_TOKEN
                    '''
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

        stage('Package App') {
            steps {
                sh '''
                zip -r app.zip .
                '''
            }
        }

        stage('Upload to Nexus') {
            steps {
                sh '''
                curl -u admin:admin123 \
                --upload-file app.zip \
                ${NEXUS_URL}/repository/${NEXUS_REPO}/app-v1.zip
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'Dockerhub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                }
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker stop python-app || true
                docker rm python-app || true
                docker run -d -p 5000:5000 --name python-app ${IMAGE_NAME}:${IMAGE_TAG}
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

    post {
        success {
            echo "🚀 Pipeline Success"
        }
        failure {
            echo "❌ Pipeline Failed"
        }
    }
}
