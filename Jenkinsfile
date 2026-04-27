pipeline {
    agent any

    environment {
        sq = "SonarQube"   // your SonarQube server name in Jenkins

        IMAGE_NAME = "python-devops-app"
        IMAGE_TAG = "latest"
        CONTAINER_NAME = "python-app"
        PORT = "5000"

        NEXUS_URL = "http://YOUR_NEXUS_IP:8081"
        NEXUS_REPO = "docker-repo"
    }

    stages {

        /* ---------------- CHECKOUT ---------------- */
        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/SatyasaiA99/python-devops-project.git'
            }
        }

        /* ---------------- SONARQUBE ANALYSIS ---------------- */
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${sq}") {
                    sh '''
                    sonar-scanner \
                    -Dsonar.projectKey=python-devops-app \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=http://YOUR_SONARQUBE_IP:9000 \
                    -Dsonar.login=YOUR_SONAR_TOKEN
                    '''
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
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        /* ---------------- STOP OLD CONTAINER ---------------- */
        stage('Stop Old Container') {
            steps {
                sh "docker stop ${CONTAINER_NAME} || true"
                sh "docker rm ${CONTAINER_NAME} || true"
            }
        }

        /* ---------------- RUN CONTAINER ---------------- */
        stage('Run Container') {
            steps {
                sh """
                docker run -d -p ${PORT}:${PORT} \
                --name ${CONTAINER_NAME} \
                ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        /* ---------------- PUSH TO NEXUS ---------------- */
        stage('Push to Nexus') {
            steps {
                sh """
                docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${NEXUS_URL}/${NEXUS_REPO}/${IMAGE_NAME}:${IMAGE_TAG}
                docker login ${NEXUS_URL} -u admin -p admin123
                docker push ${NEXUS_URL}/${NEXUS_REPO}/${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        /* ---------------- VERIFY ---------------- */
        stage('Verify') {
            steps {
                sh """
                sleep 5
                curl http://localhost:${PORT}
                """
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
